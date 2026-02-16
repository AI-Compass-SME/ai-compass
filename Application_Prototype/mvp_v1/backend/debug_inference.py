import sys
import os
# Adjust path to include project root (ai-compass)
# backend/ -> mvp_v1/ -> Application_Prototype/ -> ai-compass/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.append(project_root)

print(f"Project root: {project_root}")

try:
    from benchmarking_ai.ml_v5.inference import InferenceEngine
    print("Import OK")
    ie = InferenceEngine()
    print("Init OK")
except Exception as e:
    import traceback
    traceback.print_exc()
