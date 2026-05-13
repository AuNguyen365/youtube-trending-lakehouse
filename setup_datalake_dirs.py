import os

def create_local_datalake():
    base_path = "d:/youtube-trending-lakehouse/data"
    layers = ['bronze', 'silver', 'gold']
    
    for layer in layers:
        path = os.path.join(base_path, layer, "youtube_trending", "region=US", "dt=2023-10-01")
        os.makedirs(path, exist_ok=True)
        # Create a dummy file to keep directory in git if needed
        with open(os.path.join(path, ".gitkeep"), 'w') as f:
            pass

if __name__ == "__main__":
    create_local_datalake()
