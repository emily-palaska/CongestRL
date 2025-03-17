import cv2
import numpy as np


def save_video(figures, output_dir='../../results/plots/output_video.avi', frame_rate=1):
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    fig = figures[0]
    fig.canvas.draw()
    frame_size = (int(fig.canvas.get_width_height()[0]), int(fig.canvas.get_width_height()[1]))

    out = cv2.VideoWriter(output_dir, fourcc, frame_rate, frame_size)

    for fig in figures:
        fig.canvas.draw()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        out.write(img)

    out.release()
    cv2.destroyAllWindows()