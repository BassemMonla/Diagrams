import streamlit as st
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.analytics import Databricks, SynapseAnalytics
from diagrams.azure.storage import DataLakeStorage
from diagrams.azure.database import SQLDatabases
from diagrams.onprem.client import Users
import os

# Set page config
st.set_page_config(page_title="Architecture Diagram Generator", layout="wide")

st.title("Interactive Enterprise Medallion Architecture")
st.markdown("Use the sidebar to configure the diagram components and layout.")

# --- Sidebar Configuration ---
st.sidebar.header("Layout Options")

with st.sidebar.expander("General Layout", expanded=True):
    rankdir = st.selectbox("Orientation", ["LR", "TB"], index=0, help="LR = Left-to-Right, TB = Top-to-Bottom")
    splines = st.selectbox("Edge Style (Splines)", ["ortho", "spline", "polyline", "curved", "line"], index=0)
    nodesep = st.slider("Node Spacing", 0.5, 3.0, 0.8)
    ranksep = st.slider("Layer Spacing", 0.5, 3.0, 1.0)
    pad = st.slider("Padding", 0.1, 2.0, 0.5)
    concentrate = st.checkbox("Concentrate Edges", value=False, help="Merge overlapping edges")

with st.sidebar.expander("Styling", expanded=False):
    bgcolor = st.color_picker("Background Color", "#FFFFFF")
    fontsize = st.number_input("Font Size", min_value=10, max_value=50, value=24)
    fontname = st.text_input("Font Name", value="Sans-Serif")

st.sidebar.header("Layers to Include")
show_bronze = st.sidebar.checkbox("Bronze Layer (Raw)", value=True)
show_silver = st.sidebar.checkbox("Silver Layer (Cleaned)", value=True)
show_gold = st.sidebar.checkbox("Gold Layer (Business)", value=True)

# Graphviz attributes
graph_attr = {
    "fontsize": str(fontsize),
    "fontname": fontname,
    "bgcolor": bgcolor,
    "rankdir": rankdir,
    "splines": splines,
    "nodesep": str(nodesep),
    "ranksep": str(ranksep),
    "pad": str(pad),
    "concentrate": "true" if concentrate else "false"
}

# Output filename (without extension)
filename = "architecture_diagram"

# Generate Diagram
tab1, tab2 = st.tabs(["Architecture Diagram", "Class Model"])

with tab1:
    with st.spinner("Generating Diagram..."):
        # wrapper to prevent opening the image automatically (show=False)
        try:
            with Diagram("Enterprise Medallion Architecture", show=False, filename=filename, graph_attr=graph_attr):
                
                # 1. SOURCES
                with Cluster("Ingestion Sources", graph_attr={"bgcolor": "#EEFBFB"}):
                    source_erp = SQLDatabases("ERP System")
                    source_logs = Users("Clickstream Logs")
                    sources = [source_erp, source_logs]

                # 2. THE MEDALLION PIPELINE
                with Cluster("Azure Data Lakehouse", graph_attr={"bgcolor": "#F0F4F8", "pencolor": "#7B8894"}):
                    
                    bronze_proc = None
                    bronze_store = None
                    silver_proc = None
                    silver_store = None
                    gold_store = None

                    # BRONZE
                    if show_bronze:
                        with Cluster("Bronze Layer\n(Raw)", graph_attr={"style": "dashed"}):
                            bronze_store = DataLakeStorage("Landing Zone")
                            bronze_proc = Databricks("Ingest Job")
                    
                    # SILVER
                    if show_silver:
                        with Cluster("Silver Layer\n(Cleaned & Enriched)"):
                            silver_store = DataLakeStorage("Delta Tables")
                            silver_proc = Databricks("Transformation")

                    # GOLD
                    if show_gold:
                        with Cluster("Gold Layer\n(Business Aggregates)"):
                            gold_store = SynapseAnalytics("Data Warehouse")

                # 3. CONSUMERS
                with Cluster("Business Value"):
                    bi_tool = Users("Power BI / Tableau")

                # --- FLOW DEFINITIONS ---
                
                # Sources -> Bronze
                if show_bronze:
                    # We connect sources to bronze_proc if it exists
                    # Diagrams allows list >> node
                    sources >> Edge(label="Batch/Stream", color="darkgray") >> bronze_proc
                    
                    # Bronze Flow
                    bronze_proc >> Edge(color="firebrick") >> bronze_store

                    # Bronze -> Silver
                    if show_silver:
                        bronze_store >> Edge(label="Filter/Clean") >> silver_proc

                # Silver Flow
                if show_silver:
                    silver_proc >> Edge(color="firebrick") >> silver_store
                    
                    # Silver -> Gold
                    if show_gold:
                        silver_store >> Edge(label="Aggregate") >> gold_store

                # Gold -> BI
                if show_gold:
                    gold_store >> Edge(label="Serving", style="bold") >> bi_tool
                elif show_silver:
                    # Fallback if Gold is off but Silver is on
                    silver_store >> Edge(label="Direct Query", style="dashed") >> bi_tool
                elif show_bronze:
                    # Fallback if only Bronze is on
                    bronze_store >> Edge(label="Raw Access", style="dotted") >> bi_tool

            # Display
            # Diagram generates filename.png
            image_path = f"{filename}.png"
            if os.path.exists(image_path):
                st.image(image_path, caption="Generated Architecture", use_container_width=True)
                
                # Add download button
                with open(image_path, "rb") as file:
                    btn = st.download_button(
                            label="Download Diagram",
                            data=file,
                            file_name="architecture.png",
                            mime="image/png"
                        )
            else:
                st.error("Error: Diagram image file was not found.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

with tab2:
    st.subheader("PlantUML Class Model")
    st.markdown("This diagram represents the code structure defined in `model.puml`.")
    
    puml_image = "c:/Users/basse/diagrams/model.png"
    if os.path.exists(puml_image):
        st.image(puml_image, caption="Banking System Class Diagram", use_container_width=True)
    else:
        st.info("Image not found. Run `render_puml.py` to generate it.")
        if st.button("Generate PlantUML Image"):
            # Minimal inline render if needed, or call the script
            # For safety, we can just call the render function if we imported it, 
            # but simplest is to ask user to run the script or do it via subprocecss
            import subprocess
            try:
                subprocess.run(["python", "c:/Users/basse/diagrams/render_puml.py"], check=True)
                st.rerun()
            except Exception as e:
                st.error(f"Failed to run render script: {e}")
