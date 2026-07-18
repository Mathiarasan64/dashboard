import streamlit as st
import pandas as pd


def show_learner_profile(learner):

    months = {
        "January", "February", "March", "April", "May",
        "June", "July", "August", "September",
        "October", "November", "December"
    }

    payment_columns = [
        col for col in learner.index
        if col == "Advance" or col in months
    ]

    total_collected = 0

    for col in payment_columns:
        value = pd.to_numeric(learner[col], errors="coerce")
        if pd.notna(value):
            total_collected += value

    course_fee = float(learner["Total price"])
    outstanding = float(learner["Total Payable Fee"])

    collection_percent = (
        (total_collected / course_fee) * 100
        if course_fee > 0 else 0
    )

    st.markdown("## 👤 Learner Profile")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric("💰 Course Fee", f"₹{course_fee:,.0f}")
        st.metric("✅ Amount Collected", f"₹{total_collected:,.0f}")
        st.metric("💳 Outstanding", f"₹{outstanding:,.0f}")
        st.metric("📊 Collection %", f"{collection_percent:.1f}%")

    with col2:
        st.write(f"### {learner['Student Name']}")
        st.write(f"📧 **Email:** {learner['Email']}")
        st.write(f"📞 **Phone:** {learner['Phone No']}")
        st.write(f"💳 **Payment Type:** {learner['Payment Type']}")
        st.write(f"📅 **EMI Tenure:** {learner['Emi Tenure']}")
        st.write(f"🟢 **Status:** {learner['Learner Status']}")

    payment_type = str(learner["Payment Type"]).strip().lower()

    if payment_type != "one shot":

        st.divider()
        st.subheader("📅 Payment Timeline")

        timeline_data = []

        for month in payment_columns:

            amount = pd.to_numeric(learner[month], errors="coerce")

            if pd.isna(amount):
                amount = 0

            status = "🟢 Paid" if amount > 0 else "🔴 Pending"

            payment_link = ""

            if month != "Advance":
                link_col = f"Payment Link ({month})"

                if link_col in learner.index:
                    payment_link = learner[link_col]

            timeline_data.append({
                "Month": month,
                "Paid Amount": f"₹{amount:,.0f}",
                "Status": status,
                "Payment Link": payment_link
            })

        timeline_df = pd.DataFrame(timeline_data)

        st.data_editor(
            timeline_df,
            hide_index=True,
            use_container_width=True,
            disabled=True,
            column_config={
                "Payment Link": st.column_config.LinkColumn(
                    "Payment Link",
                    display_text="Open"
                )
            }
        )
