import streamlit as st
import pandas as pd

from database import get_analytics_data


# ============================================================
# ANALYTICS DASHBOARD
# ============================================================

def show_analytics():

    st.title("📊 Dental AI Analytics")

    st.caption(
        "Overview of assessments recorded by the Dental AI Analyzer."
    )

    # ========================================================
    # LOAD DATA
    # ========================================================

    try:

        data = get_analytics_data()

    except Exception as e:

        st.error(
            "Unable to load analytics data from Supabase."
        )

        st.exception(e)

        return


    # ========================================================
    # NO DATA
    # ========================================================

    if not data:

        st.info(
            "No assessments have been recorded yet."
        )

        return


    # ========================================================
    # DATAFRAME
    # ========================================================

    df = pd.DataFrame(data)


    # ========================================================
    # BASIC CLEANING
    # ========================================================

    if "pain_level" in df.columns:

        df["pain_level"] = pd.to_numeric(
            df["pain_level"],
            errors="coerce"
        )


    if "age" in df.columns:

        df["age"] = pd.to_numeric(
            df["age"],
            errors="coerce"
        )


    # ========================================================
    # HEADER METRICS
    # ========================================================

    total_assessments = len(df)

    average_pain = df["pain_level"].mean()

    average_age = df["age"].mean()


    # ========================================================
    # CONCERN LEVELS
    # ========================================================

    if "concern_level" in df.columns:

        concern_counts = (
            df["concern_level"]
            .fillna("Not extracted")
            .value_counts()
        )

    else:

        concern_counts = pd.Series(
            dtype="int64"
        )


    # ========================================================
    # METRIC CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total assessments",
            total_assessments
        )


    with col2:

        if pd.notna(average_pain):

            st.metric(
                "Average pain",
                f"{average_pain:.1f}/10"
            )

        else:

            st.metric(
                "Average pain",
                "N/A"
            )


    with col3:

        if pd.notna(average_age):

            st.metric(
                "Average age",
                f"{average_age:.1f}"
            )

        else:

            st.metric(
                "Average age",
                "N/A"
            )


    with col4:

        if len(concern_counts) > 0:

            most_common_concern = (
                concern_counts.index[0]
            )

            st.metric(
                "Most common concern",
                most_common_concern
            )

        else:

            st.metric(
                "Most common concern",
                "N/A"
            )


    st.divider()


    # ========================================================
    # CONCERN LEVEL ANALYSIS
    # ========================================================

    st.subheader(
        "🚨 Concern Level Distribution"
    )


    if len(concern_counts) > 0:

        concern_col1, concern_col2 = st.columns(2)


        with concern_col1:

            st.bar_chart(
                concern_counts
            )


        with concern_col2:

            st.dataframe(
                concern_counts.rename(
                    "Assessments"
                ),
                use_container_width=True
            )

    else:

        st.info(
            "No concern-level data available."
        )


    st.divider()


    # ========================================================
    # PAIN TYPE
    # ========================================================

    st.subheader(
        "🩹 Pain Type Distribution"
    )


    if "pain_type" in df.columns:

        pain_type_counts = (
            df["pain_type"]
            .fillna("Unknown")
            .value_counts()
        )

        if len(pain_type_counts) > 0:

            st.bar_chart(
                pain_type_counts
            )

            st.dataframe(
                pain_type_counts.rename(
                    "Assessments"
                ),
                use_container_width=True
            )


    st.divider()


    # ========================================================
    # PAIN LEVEL DISTRIBUTION
    # ========================================================

    st.subheader(
        "📈 Pain Level Distribution"
    )


    if "pain_level" in df.columns:

        pain_data = (
            df["pain_level"]
            .dropna()
            .value_counts()
            .sort_index()
        )

        if len(pain_data) > 0:

            st.bar_chart(
                pain_data
            )


    st.divider()


    # ========================================================
    # SYMPTOM ANALYSIS
    # ========================================================

    st.subheader(
        "🦷 Reported Symptoms"
    )


    symptom_columns = {

        "Cold sensitivity":
            "cold_sensitivity",

        "Hot sensitivity":
            "hot_sensitivity",

        "Pain while chewing":
            "chewing_pain",

        "Gum bleeding":
            "gum_bleeding",

        "Gum swelling":
            "gum_swelling",

        "Bad breath":
            "bad_breath",

        "Tooth mobility":
            "tooth_mobility",

        "Recent dental treatment":
            "recent_dental_treatment"
    }


    symptom_counts = {}


    for label, column in symptom_columns.items():

        if column in df.columns:

            symptom_counts[label] = (
                df[column]
                .fillna(False)
                .astype(bool)
                .sum()
            )


    if symptom_counts:

        symptom_series = (
            pd.Series(symptom_counts)
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            symptom_series
        )


        st.dataframe(
            symptom_series.rename(
                "Number of assessments"
            ),
            use_container_width=True
        )


    st.divider()


    # ========================================================
    # AGE DISTRIBUTION
    # ========================================================

    st.subheader(
        "👥 Age Distribution"
    )


    if "age" in df.columns:

        age_data = (
            df["age"]
            .dropna()
        )

        if len(age_data) > 0:

            age_histogram = (
                age_data
                .value_counts()
                .sort_index()
            )

            st.bar_chart(
                age_histogram
            )


    st.divider()


    # ========================================================
    # AFFECTED TEETH
    # ========================================================

    st.subheader(
        "🦷 Most Frequently Selected Teeth"
    )


    tooth_counts = {}


    if "affected_teeth" in df.columns:

        for teeth in df["affected_teeth"]:

            if teeth is None:

                continue


            if isinstance(
                teeth,
                list
            ):

                for tooth in teeth:

                    tooth = str(
                        tooth
                    )

                    tooth_counts[tooth] = (
                        tooth_counts.get(
                            tooth,
                            0
                        ) + 1
                    )


    if tooth_counts:

        tooth_series = (
            pd.Series(tooth_counts)
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            tooth_series
        )

        st.dataframe(
            tooth_series.rename(
                "Selections"
            ),
            use_container_width=True
        )

    else:

        st.info(
            "No affected-tooth data available."
        )


    st.divider()


    # ========================================================
    # RECENT ASSESSMENTS
    # ========================================================

    st.subheader(
        "🕒 Recent Assessments"
    )


    display_columns = [

        "created_at",

        "age",

        "pain_level",

        "pain_type",

        "pain_duration",

        "concern_level"
    ]


    available_columns = [

        column

        for column in display_columns

        if column in df.columns
    ]


    if available_columns:

        recent_df = df[
            available_columns
        ].head(20)


        st.dataframe(
            recent_df,
            use_container_width=True,
            hide_index=True
        )