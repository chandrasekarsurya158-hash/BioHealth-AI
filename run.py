
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    print("==========================================")
    print("       BioHealth AI Starting Up")
    print(f"       Port: {port}")
    print("==========================================")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
