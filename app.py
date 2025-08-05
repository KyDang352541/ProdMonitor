import streamlit as st
import pandas as pd

st.set_page_config(page_title="V-Tail Tracker", layout="wide")

st.title("🛠️ V-Tail Production Tracker")
st.markdown("Theo dõi tiến độ và chi phí sản xuất cho các bộ phận V-tail.")

# Tải file Excel
uploaded_file = st.file_uploader("📤 Tải file báo cáo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # Đọc dữ liệu từ file
        df_tasks = pd.read_excel(uploaded_file, sheet_name="Tasks")
        df_summary = pd.read_excel(uploaded_file, sheet_name="Summary", index_col=0)

        # Tổng quan chi phí
        st.header("📊 Tổng quan chi phí")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Giá bán", f"${df_summary.loc['Total selling price', 'Value']:,.2f}")
        col2.metric("🕒 Giờ lao động", f"{df_summary.loc['Labour hours', 'Value']}")
        col3.metric("💵 Đơn giá giờ", f"${df_summary.loc['Labour price', 'Value']:,.2f}")
        col4.metric("🧾 Đã chi", f"${df_summary.loc['Spent', 'Value']:,.2f}")

        total_cost = df_summary.loc['Labour hours', 'Value'] * df_summary.loc['Labour price', 'Value']
        total_spent = total_cost + df_summary.loc['Spent', 'Value']
        profit = df_summary.loc['Total selling price', 'Value'] - total_spent

        st.success(f"✅ **Lợi nhuận ước tính:** ${profit:,.2f}")

        # Hiển thị tiến độ công việc
        st.header("📋 Tiến độ công việc")
        for task_type in df_tasks["Type"].unique():
            st.subheader(f"🔹 {task_type}")
            df_group = df_tasks[df_tasks["Type"] == task_type].reset_index(drop=True)
            st.dataframe(df_group[["No", "Job", "Status"]], use_container_width=True)

        # Cập nhật trạng thái công việc
        st.header("✏️ Cập nhật trạng thái công việc")
        jobs = df_tasks["Job"].tolist()
        selected_job = st.selectbox("Chọn công việc:", jobs)
        new_status = st.selectbox("Trạng thái mới:", ["Done", "Inprocess", "No"])
        if st.button("Cập nhật"):
            df_tasks.loc[df_tasks["Job"] == selected_job, "Status"] = new_status
            st.success(f"Đã cập nhật trạng thái của **{selected_job}** thành **{new_status}**.")

    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file: {e}")
else:
    st.info("📥 Vui lòng tải file Excel để bắt đầu.")
