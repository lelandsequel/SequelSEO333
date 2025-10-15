"""
Streamlit UI for SEO Lead Finder
Provides manual search, automation configuration, and results dashboard
"""

import streamlit as st
import pandas as pd
import os
import sys
import subprocess
import yaml
from datetime import datetime
from pathlib import Path
import glob

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

# Page config
st.set_page_config(
    page_title="SEO Lead Finder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hot-lead {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f44336;
        margin-bottom: 1rem;
    }
    .warm-lead {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'last_results' not in st.session_state:
    st.session_state.last_results = None

def load_config():
    """Load config.yaml"""
    config_path = Path(__file__).parent / "config.yaml"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

def save_config(config):
    """Save config.yaml"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def get_latest_csv():
    """Get the most recent CSV file"""
    out_dir = Path(__file__).parent / "out"
    if not out_dir.exists():
        return None
    csv_files = list(out_dir.glob("leads_*.csv"))
    if not csv_files:
        return None
    return max(csv_files, key=lambda x: x.stat().st_mtime)

def get_latest_report():
    """Get the most recent sales report"""
    out_dir = Path(__file__).parent / "out"
    if not out_dir.exists():
        return None
    report_files = list(out_dir.glob("sales_report_*.txt"))
    if not report_files:
        return None
    return max(report_files, key=lambda x: x.stat().st_mtime)

def get_all_csvs():
    """Get all CSV files sorted by date"""
    out_dir = Path(__file__).parent / "out"
    if not out_dir.exists():
        return []
    csv_files = list(out_dir.glob("leads_*.csv"))
    return sorted(csv_files, key=lambda x: x.stat().st_mtime, reverse=True)

def normalize_dataframe(df):
    """Normalize column names for consistency"""
    # Map old column names to new standardized names
    column_mapping = {
        'Score': 'seo_score',
        'CoreWebVitals_LCP': 'lcp_score',
        'BusinessName': 'business_name',
        'Website': 'website',
        'Phone': 'phone',
        'Industry': 'industry',
        'City': 'address',
        'TechStack': 'tech_stack',
        'LLM_SEOScore': 'llm_seo_score',
        'LLM_CriticalIssues': 'llm_critical_issues',
        'LLM_RevenueImpact': 'llm_revenue_impact',
        'LLM_Opportunities': 'llm_opportunities',
        'LLM_ServicesOffered': 'llm_services_offered',
        'LLM_USP': 'llm_usp',
        'LLM_CTAQuality': 'llm_cta_quality',
        'LLM_TargetKeywords': 'llm_target_keywords',
        'LLM_MissingKeywords': 'llm_missing_keywords',
        'LLM_ContentQuality': 'llm_content_quality',
        'LLM_QuickWins': 'llm_quick_wins',
        'LLM_PitchAngle': 'llm_pitch_angle'
    }

    # Rename columns that exist
    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})

    # Create llm_summary if it doesn't exist
    if 'llm_summary' not in df.columns and 'llm_pitch_angle' in df.columns:
        df['llm_summary'] = df['llm_pitch_angle']

    return df

def run_pipeline(geo, industries=None, add_industries=None):
    """Run the lead finder pipeline"""
    cmd = ["python3", "main.py", "--once", "--geo", geo]
    
    if industries:
        cmd.extend(["--industries", industries])
    elif add_industries:
        cmd.extend(["--add-industries", add_industries])
    
    return subprocess.run(cmd, capture_output=True, text=True)

def generate_github_workflow(config):
    """Generate GitHub Actions workflow YAML"""
    schedule = config.get('automation', {}).get('schedule', {})
    day = schedule.get('day', 'monday')
    hour = schedule.get('hour', 9)
    minute = schedule.get('minute', 0)
    
    # Convert day to cron format
    day_map = {
        'monday': '1', 'tuesday': '2', 'wednesday': '3',
        'thursday': '4', 'friday': '5', 'saturday': '6', 'sunday': '0'
    }
    cron_day = day_map.get(day.lower(), '1')
    
    locations = config.get('automation', {}).get('locations', ['Houston, TX'])
    
    workflow = {
        'name': 'Weekly SEO Lead Finder',
        'on': {
            'schedule': [{'cron': f'{minute} {hour} * * {cron_day}'}],
            'workflow_dispatch': {}
        },
        'jobs': {
            'find-leads': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'name': 'Checkout code', 'uses': 'actions/checkout@v3'},
                    {'name': 'Set up Python', 'uses': 'actions/setup-python@v4', 'with': {'python-version': '3.9'}},
                    {'name': 'Install dependencies', 'run': 'pip install -r requirements.txt'},
                    {'name': 'Create secrets directory', 'run': 'mkdir -p secrets'},
                ]
            }
        }
    }
    
    # Add steps for each location
    for i, location in enumerate(locations):
        step = {
            'name': f'Find leads in {location}',
            'env': {
                'GOOGLE_PLACES_API_KEY': '${{ secrets.GOOGLE_PLACES_API_KEY }}',
                'PAGESPEED_API_KEY': '${{ secrets.PAGESPEED_API_KEY }}',
                'ANTHROPIC_API_KEY': '${{ secrets.ANTHROPIC_API_KEY }}',
                'OPENAI_API_KEY': '${{ secrets.OPENAI_API_KEY }}',
                'DATAFORSEO_LOGIN': '${{ secrets.DATAFORSEO_LOGIN }}',
                'DATAFORSEO_PASSWORD': '${{ secrets.DATAFORSEO_PASSWORD }}',
                'SLACK_WEBHOOK_URL': '${{ secrets.SLACK_WEBHOOK_URL }}'
            },
            'run': f'python3 main.py --once --geo "{location}"'
        }
        workflow['jobs']['find-leads']['steps'].append(step)
    
    # Add upload artifacts step
    workflow['jobs']['find-leads']['steps'].append({
        'name': 'Upload results',
        'uses': 'actions/upload-artifact@v3',
        'with': {
            'name': 'lead-reports',
            'path': 'out/'
        }
    })
    
    return workflow

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 SEO Lead Finder")
    st.markdown("---")
    
    # Quick stats
    config = load_config()
    automation_enabled = config.get('automation', {}).get('enabled', False)
    
    st.metric("Automation", "✅ Enabled" if automation_enabled else "❌ Disabled")
    
    latest_csv = get_latest_csv()
    if latest_csv:
        df = normalize_dataframe(pd.read_csv(latest_csv))
        st.metric("Total Leads", len(df))
        hot_leads = len(df[df['seo_score'] >= 60])
        st.metric("Hot Leads", hot_leads)
    
    st.markdown("---")
    st.markdown("### 📚 Resources")
    st.markdown("[📖 Documentation](https://github.com/lelandsequel/SequelSEO333)")
    st.markdown("[🔧 API Setup Guide](./API_SETUP_GUIDE.md)")

# Main content
tab1, tab2, tab3 = st.tabs(["🎯 Manual Search", "⏰ Automation", "📊 Results Dashboard"])

# TAB 1: Manual Search
with tab1:
    st.markdown('<div class="main-header">🎯 Find SEO Leads</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📍 Location")
        geo = st.text_input("Enter location (e.g., 'Austin, TX')", value="Austin, TX", key="manual_geo")
    
    with col2:
        st.markdown("### 🏭 Industry Mode")
        mode = st.radio(
            "Select mode",
            ["Auto-discover", "Manual", "Hybrid"],
            key="industry_mode"
        )
    
    if mode == "Manual":
        industries = st.text_input(
            "Enter industries (comma-separated)",
            value="dentists, plumbers",
            help="e.g., dentists, plumbers, roofers",
            key="manual_industries"
        )
    elif mode == "Hybrid":
        add_industries = st.text_input(
            "Add industries to auto-discovered list",
            value="",
            help="e.g., car washes, yoga studios",
            key="add_industries"
        )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🚀 Find Leads", type="primary", disabled=st.session_state.running):
            st.session_state.running = True
            
            with st.spinner("🔍 Searching for leads... This may take a few minutes..."):
                # Run pipeline
                if mode == "Manual":
                    result = run_pipeline(geo, industries=industries)
                elif mode == "Hybrid":
                    result = run_pipeline(geo, add_industries=add_industries if add_industries else None)
                else:
                    result = run_pipeline(geo)
                
                st.session_state.running = False
                
                if result.returncode == 0:
                    st.success("✅ Lead search completed!")
                    st.session_state.last_results = get_latest_csv()
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result.stderr}")
    
    with col2:
        if st.button("🔄 Refresh Results"):
            st.rerun()
    
    # Display results
    if st.session_state.last_results or get_latest_csv():
        st.markdown("---")
        st.markdown("### 📊 Latest Results")

        csv_file = st.session_state.last_results or get_latest_csv()
        df = normalize_dataframe(pd.read_csv(csv_file))
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Leads", len(df))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            hot_leads = len(df[df['seo_score'] >= 60])
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🔥 Hot Leads", hot_leads)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            warm_leads = len(df[(df['seo_score'] >= 40) & (df['seo_score'] < 60)])
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🌡️ Warm Leads", warm_leads)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            avg_score = df['seo_score'].mean()
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Score", f"{avg_score:.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Hot Leads Section
        hot_df = df[df['seo_score'] >= 60].sort_values('seo_score', ascending=False)
        
        if len(hot_df) > 0:
            st.markdown("### 🔥 Hot Leads (Score ≥ 60)")
            
            for idx, row in hot_df.iterrows():
                st.markdown(f'<div class="hot-lead">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"### {row['business_name']}")
                    st.markdown(f"🌐 [{row['website']}]({row['website']})")
                    st.markdown(f"📍 {row.get('industry', 'N/A')} • {row.get('phone', 'N/A')}")

                with col2:
                    st.metric("SEO Score", f"{row['seo_score']}/100")

                with col3:
                    st.metric("LCP", f"{row['lcp_score']:.1f}s")

                # Full detailed analysis
                with st.expander("📊 **FULL SALES INTELLIGENCE REPORT** (Click to expand)", expanded=False):
                    # Header
                    st.markdown(f"### 🎯 {row['business_name']}")
                    st.markdown(f"**Score:** {row.get('llm_seo_score', row['seo_score'])}/100 {'🔴 **CRITICAL - Immediate Action Needed**' if row['seo_score'] >= 70 else '🟡 **High Priority**'}")
                    st.markdown("---")

                    # Contact Info
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.markdown(f"📞 **Phone:** {row.get('phone', 'N/A')}")
                    with col_b:
                        st.markdown(f"🌐 **Website:** [{row['website']}]({row['website']})")
                    with col_c:
                        st.markdown(f"📍 **Location:** {row.get('address', 'N/A')}")

                    col_d, col_e = st.columns(2)
                    with col_d:
                        st.markdown(f"🏭 **Industry:** {row.get('industry', 'N/A')}")
                    with col_e:
                        st.markdown(f"💻 **Tech Stack:** {row.get('tech_stack', 'N/A')}")

                    st.markdown("---")

                    # Critical Issues
                    if pd.notna(row.get('llm_critical_issues')):
                        st.markdown("### 🔴 **CRITICAL ISSUES COSTING THEM CUSTOMERS:**")
                        st.markdown(row['llm_critical_issues'])
                        st.markdown("")

                    # Revenue Impact
                    if pd.notna(row.get('llm_revenue_impact')):
                        st.markdown("### 💰 **ESTIMATED REVENUE IMPACT:**")
                        st.markdown(row['llm_revenue_impact'])
                        st.markdown("")

                    # Opportunities
                    if pd.notna(row.get('llm_opportunities')):
                        st.markdown("### 🎯 **OPPORTUNITIES:**")
                        st.markdown(row['llm_opportunities'])
                        st.markdown("")

                    # Quick Wins
                    if pd.notna(row.get('llm_quick_wins')):
                        st.markdown("### ✅ **QUICK WINS (First 2 Weeks):**")
                        st.markdown(row['llm_quick_wins'])
                        st.markdown("")

                    # Pitch Angle
                    if pd.notna(row.get('llm_pitch_angle')):
                        st.markdown("### 💬 **PITCH ANGLE:**")
                        st.markdown(row['llm_pitch_angle'])
                        st.markdown("")

                    # Opening Call Script
                    st.markdown("### 📞 **OPENING CALL SCRIPT:**")
                    st.markdown(f'*"Hi, this is [YOUR NAME]. I was doing some research on {row.get("industry", "businesses")} in {row.get("address", "your area")} and came across {row["business_name"]}. I noticed a few things on your website that might be costing you customers – specifically your slow page speed. Do you have a couple minutes to discuss how we could fix this?"*')
                    st.markdown("")

                    # Additional Details
                    with st.expander("📋 Additional Details"):
                        if pd.notna(row.get('llm_services_offered')):
                            st.markdown(f"**Services Offered:** {row['llm_services_offered']}")
                        if pd.notna(row.get('llm_usp')):
                            st.markdown(f"**USP:** {row['llm_usp']}")
                        if pd.notna(row.get('llm_cta_quality')):
                            st.markdown(f"**CTA Quality:** {row['llm_cta_quality']}")
                        if pd.notna(row.get('llm_target_keywords')):
                            st.markdown(f"**Target Keywords:** {row['llm_target_keywords']}")
                        if pd.notna(row.get('llm_missing_keywords')):
                            st.markdown(f"**Missing Keywords:** {row['llm_missing_keywords']}")
                        if pd.notna(row.get('llm_content_quality')):
                            st.markdown(f"**Content Quality:** {row['llm_content_quality']}")

                st.markdown('</div>', unsafe_allow_html=True)
        
        # All Leads Table
        st.markdown("### 📋 All Leads")
        
        # Add filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            industry_filter = st.multiselect(
                "Filter by Industry",
                options=df['industry'].unique().tolist(),
                default=df['industry'].unique().tolist()
            )
        
        with col2:
            min_score = st.slider("Min SEO Score", 0, 100, 0)
        
        with col3:
            max_lcp = st.slider("Max LCP (seconds)", 0.0, 50.0, 50.0)
        
        # Apply filters
        filtered_df = df[
            (df['industry'].isin(industry_filter)) &
            (df['seo_score'] >= min_score) &
            (df['lcp_score'] <= max_lcp)
        ]
        
        st.dataframe(
            filtered_df[['business_name', 'industry', 'website', 'seo_score', 'lcp_score', 'phone']],
            use_container_width=True,
            hide_index=True
        )
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            report_file = get_latest_report()
            if report_file:
                with open(report_file, 'r') as f:
                    report_data = f.read()
                st.download_button(
                    label="📊 Download Sales Report",
                    data=report_data,
                    file_name=f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

# TAB 2: Automation
with tab2:
    st.markdown('<div class="main-header">⏰ Automation Settings</div>', unsafe_allow_html=True)
    
    config = load_config()
    automation_config = config.get('automation', {})
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ⚙️ Configure Weekly Automation")
        
        enabled = st.checkbox(
            "Enable weekly automation",
            value=automation_config.get('enabled', False),
            help="When enabled, the system will automatically search for leads every week"
        )
        
        st.markdown("#### 📅 Schedule")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            day = st.selectbox(
                "Day of week",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                index=0 if not automation_config.get('schedule') else 
                      ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(
                          automation_config.get('schedule', {}).get('day', 'Monday').title()
                      )
            )
        
        with col_b:
            hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, 
                                  value=automation_config.get('schedule', {}).get('hour', 9))
        
        with col_c:
            minute = st.number_input("Minute (0-59)", min_value=0, max_value=59,
                                    value=automation_config.get('schedule', {}).get('minute', 0))
        
        st.info(f"📅 Automation will run every {day} at {hour:02d}:{minute:02d} UTC")

        st.markdown("#### 📍 Locations")
        locations_text = st.text_area(
            "Enter locations (one per line)",
            value="\n".join(automation_config.get('locations', ['Houston, TX'])),
            help="Each location will be searched separately",
            height=100
        )
        locations = [loc.strip() for loc in locations_text.split('\n') if loc.strip()]

        st.markdown("#### 🏭 Industry Settings")
        auto_mode = st.radio(
            "Industry discovery mode",
            ["Auto-discover", "Manual", "Hybrid"],
            index=0,
            help="Auto-discover: AI finds top industries. Manual: You specify. Hybrid: Both."
        )

        if auto_mode == "Manual":
            manual_industries = st.text_input(
                "Industries (comma-separated)",
                value=automation_config.get('industries', 'dentists, plumbers, roofers'),
                help="e.g., dentists, plumbers, roofers"
            )
        elif auto_mode == "Hybrid":
            hybrid_industries = st.text_input(
                "Additional industries (comma-separated)",
                value=automation_config.get('add_industries', ''),
                help="These will be added to auto-discovered industries"
            )

        st.markdown("#### 🔔 Notifications")

        slack_enabled = st.checkbox(
            "Send Slack notifications",
            value=automation_config.get('slack_enabled', False),
            help="Requires SLACK_WEBHOOK_URL in .env"
        )

        if slack_enabled:
            st.info("💡 Make sure SLACK_WEBHOOK_URL is set in your GitHub Secrets")

    with col2:
        st.markdown("### 📊 Automation Status")

        if enabled:
            st.success("✅ Automation is ENABLED")
        else:
            st.warning("⚠️ Automation is DISABLED")

        st.markdown("---")

        st.markdown("### 🔧 Quick Actions")

        if st.button("💾 Save Settings", type="primary"):
            # Update config
            new_config = config.copy()
            new_config['automation'] = {
                'enabled': enabled,
                'schedule': {
                    'day': day.lower(),
                    'hour': hour,
                    'minute': minute
                },
                'locations': locations,
                'mode': auto_mode.lower().replace('-', '_'),
                'slack_enabled': slack_enabled
            }

            if auto_mode == "Manual":
                new_config['automation']['industries'] = manual_industries
            elif auto_mode == "Hybrid":
                new_config['automation']['add_industries'] = hybrid_industries

            # Save config
            save_config(new_config)

            # Generate GitHub workflow
            workflow = generate_github_workflow(new_config)
            workflow_path = Path(__file__).parent / ".github" / "workflows" / "weekly.yml"
            workflow_path.parent.mkdir(parents=True, exist_ok=True)

            with open(workflow_path, 'w') as f:
                yaml.dump(workflow, f, default_flow_style=False, sort_keys=False)

            st.success("✅ Settings saved!")
            st.info("💡 Don't forget to commit and push the updated workflow file to GitHub")

            # Show git commands
            with st.expander("📝 Git Commands to Run"):
                st.code(f"""
git add .github/workflows/weekly.yml config.yaml
git commit -m "Update automation settings: {day} at {hour:02d}:{minute:02d}"
git push origin main
                """, language="bash")

        if st.button("🧪 Test Automation Now"):
            st.info("🚀 Running test automation...")

            with st.spinner("Running automation test..."):
                # Run for first location only
                if locations:
                    result = run_pipeline(locations[0])

                    if result.returncode == 0:
                        st.success(f"✅ Test completed for {locations[0]}")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result.stderr}")
                else:
                    st.error("❌ No locations configured")

        st.markdown("---")

        st.markdown("### 📚 Setup Guide")

        with st.expander("🔑 GitHub Secrets Required"):
            st.markdown("""
            Make sure these secrets are set in your GitHub repository:

            **Settings → Secrets and variables → Actions → New repository secret**

            Required secrets:
            - `GOOGLE_PLACES_API_KEY`
            - `PAGESPEED_API_KEY`
            - `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
            - `DATAFORSEO_LOGIN`
            - `DATAFORSEO_PASSWORD`

            Optional:
            - `SLACK_WEBHOOK_URL` (for notifications)
            - `GOOGLE_SERVICE_ACCOUNT_JSON` (for Sheets integration)
            """)

        with st.expander("📖 How It Works"):
            st.markdown("""
            1. **Configure** your schedule and locations above
            2. **Save Settings** to generate the GitHub Actions workflow
            3. **Commit and push** the workflow file to GitHub
            4. **GitHub Actions** will run automatically on your schedule
            5. **Results** are saved as artifacts in GitHub Actions
            6. **Notifications** sent to Slack (if enabled)

            You can also manually trigger the workflow from GitHub Actions tab.
            """)

# TAB 3: Results Dashboard
with tab3:
    st.markdown('<div class="main-header">📊 Results Dashboard</div>', unsafe_allow_html=True)

    all_csvs = get_all_csvs()

    if not all_csvs:
        st.info("📭 No results yet. Run a manual search or wait for automation to complete.")
    else:
        st.markdown(f"### 📁 Found {len(all_csvs)} result files")

        # File selector
        selected_file = st.selectbox(
            "Select a results file",
            options=all_csvs,
            format_func=lambda x: f"{x.stem} ({datetime.fromtimestamp(x.stat().st_mtime).strftime('%Y-%m-%d %H:%M')})"
        )

        if selected_file:
            df = normalize_dataframe(pd.read_csv(selected_file))

            # Summary metrics
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Total Leads", len(df))

            with col2:
                hot = len(df[df['seo_score'] >= 60])
                st.metric("🔥 Hot", hot)

            with col3:
                warm = len(df[(df['seo_score'] >= 40) & (df['seo_score'] < 60)])
                st.metric("🌡️ Warm", warm)

            with col4:
                cold = len(df[df['seo_score'] < 40])
                st.metric("❄️ Cold", cold)

            with col5:
                avg_score = df['seo_score'].mean()
                st.metric("Avg Score", f"{avg_score:.1f}")

            st.markdown("---")

            # Charts
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📊 Leads by Industry")
                industry_counts = df['industry'].value_counts()
                st.bar_chart(industry_counts)

            with col2:
                st.markdown("#### 📈 Score Distribution")
                score_bins = pd.cut(df['seo_score'], bins=[0, 40, 60, 100], labels=['Cold', 'Warm', 'Hot'])
                score_counts = score_bins.value_counts()
                st.bar_chart(score_counts)

            st.markdown("---")

            # Data table
            st.markdown("#### 📋 All Leads")

            # Filters
            col1, col2, col3 = st.columns(3)

            with col1:
                industries = st.multiselect(
                    "Industries",
                    options=df['industry'].unique().tolist(),
                    default=df['industry'].unique().tolist(),
                    key="dashboard_industries"
                )

            with col2:
                score_range = st.slider(
                    "SEO Score Range",
                    0, 100, (0, 100),
                    key="dashboard_score"
                )

            with col3:
                lcp_max = st.slider(
                    "Max LCP (seconds)",
                    0.0, 50.0, 50.0,
                    key="dashboard_lcp"
                )

            # Apply filters
            filtered = df[
                (df['industry'].isin(industries)) &
                (df['seo_score'] >= score_range[0]) &
                (df['seo_score'] <= score_range[1]) &
                (df['lcp_score'] <= lcp_max)
            ]

            st.dataframe(
                filtered[['business_name', 'industry', 'website', 'seo_score', 'lcp_score', 'phone', 'address']],
                use_container_width=True,
                hide_index=True
            )

            # Export
            col1, col2 = st.columns(2)

            with col1:
                csv_data = filtered.to_csv(index=False)
                st.download_button(
                    label=f"📥 Download Filtered Results ({len(filtered)} leads)",
                    data=csv_data,
                    file_name=f"filtered_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

            with col2:
                # Find corresponding report
                file_date = selected_file.stem.split('_')[1]
                report_pattern = f"sales_report_*_{file_date[:8]}*.txt"
                report_files = list((Path(__file__).parent / "out").glob(report_pattern))

                if report_files:
                    with open(report_files[0], 'r') as f:
                        report_data = f.read()
                    st.download_button(
                        label="📊 Download Sales Report",
                        data=report_data,
                        file_name=f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🎯 SEO Lead Finder | Built with Streamlit |
    <a href="https://github.com/lelandsequel/SequelSEO333" target="_blank">GitHub</a>
    </p>
</div>
""", unsafe_allow_html=True)


