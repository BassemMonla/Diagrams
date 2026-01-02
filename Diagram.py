from diagrams import Diagram, Cluster, Edge
# --- Import specific icons here ---
# Browse all available icons at: https://diagrams.mingrammer.com/docs/nodes/aws
from diagrams.azure.analytics import Databricks, SynapseAnalytics
from diagrams.azure.storage import DataLakeStorage
from diagrams.azure.database import SQLDatabases
from diagrams.onprem.client import Users
from diagrams.custom import Custom

# --- Configuration for "Visio" look ---
graph_attr = {
    "fontsize": "24",
    "bgcolor": "white",
    "rankdir": "LR",       # LR = Left-to-Right, TB = Top-to-Bottom
    "splines": "ortho",    # "ortho" gives you right-angled (Visio-like) connectors
    "nodesep": "0.8",      # Increase space between nodes
    "ranksep": "1.0",      # Increase space between layers
    "pad": "0.5"
}

with Diagram("Enterprise Medallion Architecture", show=True, graph_attr=graph_attr):

    # 1. SOURCES
    with Cluster("Ingestion Sources", graph_attr={"bgcolor": "#EEFBFB"}):
        sources = [
            SQLDatabases("ERP System"), 
            Users("Clickstream Logs")
        ]

    # 2. THE MEDALLION PIPELINE
    # We use a main cluster to group the Data Lakehouse components
    with Cluster("Azure Data Lakehouse", graph_attr={"bgcolor": "#F0F4F8", "pencolor": "#7B8894"}):
        
        # BRONZE LAYER
        with Cluster("Bronze Layer\n(Raw)", graph_attr={"style": "dashed"}):
            bronze_store = DataLakeStorage("Landing Zone")
            bronze_proc = Databricks("Ingest Job")
            
        # SILVER LAYER
        with Cluster("Silver Layer\n(Cleaned & Enriched)"):
            silver_store = DataLakeStorage("Delta Tables")
            silver_proc = Databricks("Transformation")

        # GOLD LAYER
        with Cluster("Gold Layer\n(Business Aggregates)"):
            gold_store = SynapseAnalytics("Data Warehouse")

    # 3. DOWNSTREAM CONSUMERS
    with Cluster("Business Value"):
        # You can name the edges to describe the data moving through
        bi_tool = Users("Power BI / Tableau")

    # --- DEFINING THE FLOW ---
    
    # Connect Sources to Bronze
    sources >> Edge(label="Batch/Stream", color="darkgray") >> bronze_proc
    
    # Internal Medallion Flow
    bronze_proc >> Edge(color="firebrick") >> bronze_store
    bronze_store >> Edge(label="Filter/Clean") >> silver_proc
    silver_proc >> Edge(color="firebrick") >> silver_store
    silver_store >> Edge(label="Aggregate") >> gold_store
    
    # Connect to BI
    gold_store >> Edge(label="Serving", style="bold") >> bi_tool