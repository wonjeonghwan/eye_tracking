# main.py
from eye_tracker import run_eye_tracker
from face_mesh_viewer import run_face_mesh_viewer

if __name__ == "__main__":
    USE_EYE_TRACKING = True
    USE_FACE_MESH = False

    if USE_EYE_TRACKING:
        run_eye_tracker(show_face_mesh=True)  # True: 얼굴 메쉬도 함께, False: 시선 추적만
    elif USE_FACE_MESH:
        run_face_mesh_viewer()