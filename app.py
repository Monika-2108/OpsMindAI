
import streamlit as st
from datetime import datetime

from database.db import (
    initialize_database,
    save_incident,
    save_suggestion,
    update_incident,
    get_all_incidents,
    get_incident,
    get_incident_count,
    get_resolved_count
)

from modules.incident_analyzer import analyze_incident

from modules.learning import (
    remember_resolved_incident,
    find_similar_incidents,
    generate_learning_insights
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="OpsMind AI",
    page_icon="ðŸ§ ",
    layout="wide"
)

initialize_database()


# --------------------------------------------------
# ORIGINAL VIOLET & MAGENTA THEME
# --------------------------------------------------

st.markdown("""
<style>

/* Main application */

.stApp,
[data-testid="stAppViewContainer"] {
    background-color: #18111F;
    color: #F9E9FC;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}


/* Sidebar */

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background-color: #211628;
}

[data-testid="stSidebar"] {
    border-right: 1px solid #392344;
}

[data-testid="stSidebar"] h1 {
    color: #F9E9FC;
    font-size: 1.65rem;
    font-weight: 750;
}

[data-testid="stSidebar"] p {
    color: #A98BB3;
}


/* Headings and text */

h1, h2, h3, h4 {
    color: #F9E9FC !important;
    font-weight: 700;
}

h1 {
    letter-spacing: -0.7px;
}

p, label, li {
    color: #DCCBE2;
}


/* Sidebar navigation */

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 8px;
}

[data-testid="stSidebar"] [role="radio"] {
    background-color: transparent;
    border-radius: 9px;
    padding: 9px 12px;
    transition: background-color 0.2s ease;
}

[data-testid="stSidebar"] [role="radio"]:hover {
    background-color: #34213E;
}

[data-testid="stSidebar"] [role="radio"]:has(input:checked) {
    background-color: #392344;
    border: 1px solid #75418A;
}


/* Buttons */

.stButton > button,
.stFormSubmitButton > button {
    background-color: #C34DDB;
    color: #FFFFFF;
    border: 1px solid #D16BE5;
    border-radius: 9px;
    padding: 0.55rem 1rem;
    font-weight: 650;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #AD3CC6;
    color: #FFFFFF;
    border: 1px solid #DF8BEC;
    box-shadow: 0 4px 16px rgba(195, 77, 219, 0.18);
}

.stButton > button:focus,
.stFormSubmitButton > button:focus {
    box-shadow: 0 0 0 2px #F9E9FC;
}


/* Metric cards */

[data-testid="stMetric"] {
    background-color: #281A30;
    border: 1px solid #493052;
    padding: 20px;
    border-radius: 13px;
    min-height: 120px;
}

[data-testid="stMetricLabel"] {
    color: #C7A9D0 !important;
}

[data-testid="stMetricValue"] {
    color: #F9E9FC !important;
    font-weight: 750;
}

[data-testid="stMetricDelta"] {
    color: #D78BE8 !important;
}


/* Containers and cards */

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #281A30;
    border: 1px solid #493052;
    border-radius: 13px;
}


/* Expanders */

[data-testid="stExpander"] {
    background-color: #281A30;
    border: 1px solid #493052;
    border-radius: 12px;
}

[data-testid="stExpander"] summary {
    color: #F9E9FC;
    font-weight: 600;
}


/* Input visibility */

div[data-baseweb="input"],
div[data-baseweb="textarea"] {
    background-color: #281A30 !important;
    border: 1px solid #60406C !important;
    border-radius: 9px !important;
}

[data-testid="stTextInput"] input,
div[data-baseweb="input"] input,
input[type="text"] {
    background-color: #281A30 !important;
    color: #F9E9FC !important;
    -webkit-text-fill-color: #F9E9FC !important;
    caret-color: #F9E9FC !important;
    opacity: 1 !important;
}

[data-testid="stTextArea"] textarea,
div[data-baseweb="textarea"] textarea,
textarea {
    background-color: #281A30 !important;
    background: #281A30 !important;
    color: #F9E9FC !important;
    -webkit-text-fill-color: #F9E9FC !important;
    caret-color: #F9E9FC !important;
    opacity: 1 !important;
    border-radius: 8px !important;
    color-scheme: dark;
}

[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stTextInput"] input::placeholder,
textarea::placeholder,
input::placeholder {
    color: #A98BB3 !important;
    -webkit-text-fill-color: #A98BB3 !important;
    opacity: 1 !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="textarea"]:focus-within {
    border-color: #C34DDB !important;
    box-shadow: 0 0 0 1px #C34DDB !important;
}


/* Select boxes */

[data-baseweb="select"] > div {
    background-color: #281A30 !important;
    border-color: #60406C !important;
    border-radius: 9px !important;
}

[data-baseweb="select"] * {
    color: #F9E9FC !important;
}


/* Form elements */

[data-testid="stForm"] {
    background-color: #211628;
    border: 1px solid #493052;
    border-radius: 13px;
    padding: 22px;
}


/* Tabs */

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    border-bottom: 1px solid #493052;
}

.stTabs [data-baseweb="tab"] {
    color: #C7A9D0;
}

.stTabs [aria-selected="true"] {
    color: #E5A0F2 !important;
    border-bottom-color: #C34DDB !important;
}


/* Dividers */

hr {
    border-color: #493052 !important;
}


/* --------------------------------------------------
   ALERT VISIBILITY FIX
   Applies to warning, success, error and info messages.
-------------------------------------------------- */

div[data-testid="stAlert"] {
    background: #281A30 !important;
    background-color: #281A30 !important;
    border: 1px solid #75418A !important;
    border-radius: 10px !important;
    color: #F9E9FC !important;
}

/* Keep nested alert containers transparent */

div[data-testid="stAlert"] > div,
div[data-testid="stAlert"] [data-testid="stAlertContent"] {
    background: transparent !important;
    background-color: transparent !important;
}

/* Force readable text throughout each alert */

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] label,
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"],
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
    color: #F9E9FC !important;
    -webkit-text-fill-color: #F9E9FC !important;
}

/* Keep alert icons visible */

div[data-testid="stAlert"] svg {
    color: #D78BE8 !important;
    fill: none;
}


/* Links */

a {
    color: #DF8BEC !important;
}


/* Spinner */

.stSpinner > div {
    border-top-color: #C34DDB !important;
}


/* Scrollbar */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #18111F;
}

::-webkit-scrollbar-thumb {
    background: #60406C;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #C34DDB;
}


/* Footer */

.opsmind-footer {
    color: #A98BB3;
    font-size: 0.82rem;
    text-align: center;
    padding: 12px 5px;
    border-top: 1px solid #493052;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.markdown("# ðŸ§  OpsMind AI")

st.sidebar.caption(
    "Intelligent Incident Learning System"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "New Incident",
        "Incident History",
        "Memory Centre",
        "Learning Insights"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Powered by Groq + Hindsight"
)


# --------------------------------------------------
# HELPER
# --------------------------------------------------

def show_incident_details(incident):
    st.write(f"**Incident:** {incident['title']}")
    st.write(f"**Severity:** {incident['severity']}")
    st.write(f"**Description:** {incident['description']}")


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "Overview":

    st.title("OpsMind AI")

    st.subheader(
        "Every incident teaches. Every resolution makes the next decision better."
    )

    st.caption(
        "Your intelligent incident monitoring and learning workspace."
    )

    incidents = get_all_incidents()

    total = len(incidents)

    resolved = sum(
        1 for incident in incidents
        if incident["outcome"] == "Resolved"
    )

    pending = sum(
        1 for incident in incidents
        if incident["outcome"] == "Pending"
    )

    failed = sum(
        1 for incident in incidents
        if incident["outcome"] == "Failed"
    )

    partially_resolved = sum(
        1 for incident in incidents
        if incident["outcome"] == "Partially Resolved"
    )

    success_rate = (
        resolved / total * 100
        if total else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Incidents", total)
    col2.metric("Resolved Incidents", resolved)
    col3.metric("Pending Incidents", pending)
    col4.metric("Resolution Success Rate", f"{success_rate:.1f}%")

    st.markdown("---")

    st.subheader("Incident Severity Breakdown")

    severity_levels = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    severity_counts = {
        level: sum(
            1 for incident in incidents
            if str(incident["severity"]).strip().lower() == level.lower()
        )
        for level in severity_levels
    }

    severity_columns = st.columns(4)

    for column, level in zip(severity_columns, severity_levels):
        column.metric(
            f"{level} Severity",
            severity_counts[level]
        )

    st.subheader("Resolution Overview")

    outcome_columns = st.columns(3)

    outcome_columns[0].metric("Resolved", resolved)
    outcome_columns[1].metric("Failed", failed)
    outcome_columns[2].metric("Partially Resolved", partially_resolved)

    st.caption(
        "Resolution success rate = Resolved incidents ÷ Total incidents. "
        "Pending, failed and partially resolved incidents are not counted as successful."
    )

    st.markdown("---")

    st.subheader("Incident Trend")

    daily_counts = {}

    for incident in incidents:

        created_at = incident["created_at"]

        if not created_at:
            continue

        try:
            incident_date = datetime.fromisoformat(
                str(created_at).replace("Z", "+00:00")
            ).date()

        except (ValueError, TypeError):
            continue

        daily_counts[incident_date] = (
            daily_counts.get(incident_date, 0) + 1
        )

    if daily_counts:

        recent_dates = sorted(daily_counts.keys())[-7:]

        trend_data = {
            "Date": [
                day.strftime("%d %b")
                for day in recent_dates
            ],
            "Incidents": [
                daily_counts[day]
                for day in recent_dates
            ]
        }

        st.bar_chart(
            trend_data,
            x="Date",
            y="Incidents",
            width='stretch'
        )

    else:
        st.info(
            "Incident trend will appear here when records with valid "
            "creation dates are available."
        )

    st.markdown("---")

    st.subheader("Recent Activity")

    if incidents:

        for incident in incidents[:5]:

            with st.container(border=True):

                activity_col1, activity_col2 = st.columns([3, 1])

                with activity_col1:

                    st.markdown(
                        f"**#{incident['id']} — {incident['title']}**"
                    )

                    st.caption(
                        f"Severity: {incident['severity']} "
                        f"| Created: {incident['created_at']}"
                    )

                with activity_col2:

                    outcome = incident["outcome"] or "Pending"
                    st.markdown(f"**{outcome}**")

    else:
        st.info(
            "No incidents recorded yet. Submit your first incident."
        )

    st.markdown("---")

    st.subheader("How OpsMind AI Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 01 — Analyze")
        st.write(
            "Groq analyzes new incidents and suggests troubleshooting steps."
        )

    with col2:
        st.markdown("### 02 — Remember")
        st.write(
            "Hindsight stores real incident experiences and resolutions."
        )

    with col3:
        st.markdown("### 03 — Learn")
        st.write(
            "The agent recalls previous experiences to improve future decisions."
        )


# --------------------------------------------------
# NEW INCIDENT
# --------------------------------------------------

elif page == "New Incident":

    st.title("Report a New Incident")

    st.write(
        "Describe the problem. OpsMind will search its experience "
        "and analyze the incident."
    )

    with st.form("incident_form"):

        title = st.text_input(
            "Incident Title",
            placeholder="Example: Payment API timeout after deployment"
        )

        description = st.text_area(
            "Incident Description",
            placeholder=(
                "Describe what happened, error messages, "
                "affected services and recent changes..."
            ),
            height=160
        )

        severity = st.selectbox(
            "Severity",
            ["Low", "Medium", "High", "Critical"]
        )

        submitted = st.form_submit_button(
            "Analyze Incident",
            width="stretch"
        )

    if submitted:

        if not title.strip() or not description.strip():

            st.error("Please enter both title and description.")

        else:

            with st.spinner("Searching previous incident experiences..."):

                try:
                    memories = find_similar_incidents(
                        f"{title}. {description}"
                    )

                except Exception as error:
                    memories = None
                    st.warning(
                        f"Memory recall unavailable: {error}"
                    )

            if isinstance(memories, list) and memories:

                st.markdown("---")
                st.subheader("Previous Incident Intelligence")

                displayed = 0

                for memory in memories:

                    if not isinstance(memory, dict):
                        continue

                    incident = memory.get("incident", {})

                    if not isinstance(incident, dict):
                        continue

                    displayed += 1

                    outcome = incident.get("outcome") or "Pending"
                    root_cause = incident.get("root_cause") or ""
                    solution = incident.get("actual_solution") or ""

                    with st.container(border=True):

                        st.markdown(
                            f"**{incident.get('title', 'Previous Incident')}**"
                        )

                        col1, col2, col3 = st.columns(3)

                        col1.metric(
                            "Incident ID",
                            f"#{incident.get('id', 'N/A')}"
                        )

                        col2.metric(
                            "Severity",
                            incident.get("severity", "Unknown")
                        )

                        col3.metric("Status", outcome)

                        if root_cause:
                            st.markdown("**Confirmed Root Cause**")
                            st.write(root_cause)

                        if solution and outcome.lower() == "resolved":
                            st.success(
                                f"Previously successful solution: {solution}"
                            )

                        elif outcome.lower() != "resolved":
                            st.warning(
                                "This incident is not resolved. "
                                "Do not treat its suggested actions as confirmed solutions."
                            )

                if displayed == 0:
                    st.info("No displayable previous incident records found.")

            else:
                st.info(
                    "No previous matching incident records were found. "
                    "Groq will analyze this incident using the available details."
                )

            # Keep full matches for the UI, but send only confirmed learning to Groq.
            memories_for_analysis = None

            if isinstance(memories, list):
                resolved_context = []

                for memory in memories:
                    if not isinstance(memory, dict):
                        continue

                    incident = memory.get("incident", {})

                    if not isinstance(incident, dict):
                        continue

                    if str(incident.get("outcome", "")).lower() == "resolved":
                        resolved_context.append(
                            "Previous resolved incident: "
                            + str(incident.get("title", ""))[:120]
                            + "\\nConfirmed root cause: "
                            + str(incident.get("root_cause", ""))[:400]
                            + "\\nSuccessful solution: "
                            + str(incident.get("actual_solution", ""))[:700]
                        )

                if resolved_context:
                    memories_for_analysis = "\\n\\n".join(
                        resolved_context[:1]
                    )

            incident_id = save_incident(
                title.strip(),
                description.strip(),
                severity
            )

            with st.spinner("Groq is analyzing the incident..."):

                try:
                    suggestion = analyze_incident(
                        title=title,
                        description=description,
                        severity=severity,
                        previous_memories=memories_for_analysis
                    )

                    save_suggestion(
                        incident_id,
                        suggestion
                    )

                    st.session_state["last_incident_id"] = incident_id
                    st.session_state["last_suggestion"] = suggestion

                    st.success(
                        f"Incident #{incident_id} analyzed successfully."
                    )

                except Exception as error:
                    st.error(str(error))

    if "last_suggestion" in st.session_state:

        st.markdown("---")
        st.subheader("AI Incident Analysis")

        st.markdown(
            st.session_state["last_suggestion"]
        )

        st.info(
            "These are AI-generated recommendations. "
            "Verify them before performing operational actions."
        )

        st.write(
            f"Incident ID: #{st.session_state['last_incident_id']}"
        )


elif page == "Incident History":

    st.title("Incident History")

    st.caption(
        "Review previous incidents, AI recommendations and final resolutions."
    )

    incidents = get_all_incidents()

    if not incidents:
        st.info("No incidents available yet.")

    else:

        for incident in incidents:

            with st.expander(
                f"#{incident['id']} — {incident['title']} "
                f"({incident['outcome']})"
            ):

                show_incident_details(incident)

                st.markdown("**AI Suggested Solution**")
                st.write(
                    incident["suggested_solution"] or "Not available"
                )

                st.markdown("**Actual Solution**")
                st.write(
                    incident["actual_solution"] or "Not recorded"
                )

                st.markdown("**Root Cause**")
                st.write(
                    incident["root_cause"] or "Not confirmed"
                )

                st.markdown("---")

                if incident["outcome"] == "Pending":

                    st.markdown("### Record Final Resolution")

                    with st.form(
                        f"resolution_form_{incident['id']}"
                    ):

                        actual_solution = st.text_area(
                            "What action did you actually take?"
                        )

                        outcome = st.selectbox(
                            "Outcome",
                            [
                                "Resolved",
                                "Failed",
                                "Partially Resolved"
                            ],
                            key=f"outcome_{incident['id']}"
                        )

                        root_cause = st.text_area(
                            "Confirmed Root Cause"
                        )

                        submitted = st.form_submit_button(
                            "Save Resolution"
                        )

                    if submitted:

                        if not actual_solution.strip():

                            st.error(
                                "Please describe the actual action taken."
                            )

                        elif not root_cause.strip():

                            st.error(
                                "Please enter the root cause, "
                                "or explain what is still unknown."
                            )

                        else:

                            update_incident(
                                incident["id"],
                                actual_solution,
                                outcome,
                                root_cause
                            )

                            updated_incident = get_incident(
                                incident["id"]
                            )

                            try:

                                if outcome == "Resolved":

                                    remember_resolved_incident(
                                        updated_incident
                                    )

                                    st.success(
                                        "Resolution saved and experience "
                                        "sent to Hindsight memory."
                                    )

                                else:
                                    st.success(
                                        "Incident outcome saved."
                                    )

                            except Exception as error:

                                st.warning(
                                    "Incident saved locally, but Hindsight "
                                    f"memory update failed: {error}"
                                )

                            st.rerun()


# --------------------------------------------------
# MEMORY CENTRE
# --------------------------------------------------

elif page == "Memory Centre":

    st.title("Hindsight Memory Centre")

    st.write(
        "Search previous incident experiences stored by OpsMind AI."
    )

    query = st.text_area(
        "What incident or problem should OpsMind remember?",
        placeholder="Example: Payment API timeout after deployment"
    )

    if st.button("Recall Previous Experiences"):

        if not query.strip():
            st.warning("Enter a search query.")

        else:
            with st.spinner("Recalling stored experiences..."):

                try:
                    memories = find_similar_incidents(query)

                    st.subheader("Retrieved Experiences")

                    if isinstance(memories, list) and memories:

                        st.caption(
                            f"{len(memories)} matching incident(s) found."
                        )

                        for index, memory in enumerate(memories, start=1):

                            if not isinstance(memory, dict):
                                continue

                            incident = memory.get("incident", {})

                            if not isinstance(incident, dict):
                                continue

                            with st.container(border=True):

                                st.markdown(
                                    f"### {index}. {incident.get('title', 'Untitled Incident')}"
                                )

                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.caption("INCIDENT ID")
                                    st.write(f"#{incident.get('id', 'N/A')}")

                                with col2:
                                    st.caption("SEVERITY")
                                    st.write(incident.get('severity', 'Not specified'))

                                with col3:
                                    st.caption("STATUS")
                                    st.write(incident.get('outcome') or 'Pending')

                                st.caption(
                                    f"Source: {memory.get('source', 'Incident Memory')}"
                                )

                                if memory.get("match_score") is not None:
                                    st.caption(
                                        f"Match score: {memory['match_score']}"
                                    )

                                if incident.get("description"):
                                    st.markdown("**Incident Description**")
                                    st.write(incident["description"])

                                st.divider()

                                st.markdown("**Confirmed Root Cause**")

                                if incident.get("root_cause"):
                                    st.write(incident["root_cause"])
                                else:
                                    st.info("Root cause has not been confirmed yet.")

                                st.markdown("**Actual Solution Used**")

                                if incident.get("actual_solution"):
                                    st.success(incident["actual_solution"])
                                else:
                                    st.info("No confirmed solution recorded yet.")

                    elif isinstance(memories, list):
                        st.info("No matching incident experiences were found.")

                    else:
                        st.info(
                            "The memory service returned a result "
                            "that could not be displayed as incident cards."
                        )

                except Exception as error:
                    st.error(f"Memory recall failed: {error}")


# LEARNING INSIGHTS
# --------------------------------------------------

elif page == "Learning Insights":

    st.title("Learning Insights")

    st.write(
        "Ask Hindsight to reflect on stored incident experiences "
        "and identify useful operational patterns."
    )

    question = st.text_area(
        "What should OpsMind learn from its incident history?",
        placeholder=(
            "Example: What recurring causes are appearing "
            "in our payment API incidents?"
        )
    )

    if st.button("Generate Learning Insights"):

        if not question.strip():
            st.warning("Enter a question first.")

        else:

            with st.spinner(
                "Hindsight is reflecting on stored experiences..."
            ):

                try:
                    insights = generate_learning_insights(
                        question
                    )

                    st.subheader("Learning Results")
                    st.write(insights)

                except Exception as error:
                    st.error(
                        f"Learning reflection failed: {error}"
                    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.caption(
    "OpsMind AI | Incident Learning Agent"
)

st.markdown(
    """
    <div class="opsmind-footer">
        OpsMind AI · Intelligent Incident Learning · Powered by Groq + Hindsight
    </div>
    """,
    unsafe_allow_html=True
)
