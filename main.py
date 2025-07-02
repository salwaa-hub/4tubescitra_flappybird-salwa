import sys, time, random, pygame
from collections import deque
import cv2 as cv, mediapipe as mp

# ==== Fungsi High Score ====
HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

# ==== MediaPipe Setup ====
mp_face_mesh = mp.solutions.face_mesh

# ==== Pygame Setup ====
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/sneaky-guitar-loop.mp3")
pygame.mixer.music.play(-1)

sound_start = pygame.mixer.Sound("assets/game-start.mp3")
sound_point = pygame.mixer.Sound("assets/point.mp3")
sound_hit = pygame.mixer.Sound("assets/punch-impact.mp3")
sound_gameover = pygame.mixer.Sound("assets/game-over.mp3")
sound_start.play()

# ==== Webcam & Display ====
VID_CAP = cv.VideoCapture(0)
window_size = (int(VID_CAP.get(cv.CAP_PROP_FRAME_WIDTH)), int(VID_CAP.get(cv.CAP_PROP_FRAME_HEIGHT)))
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Flippy Bird Face Control")

# ==== Sprites ====
bird_img = pygame.image.load("assets/bird_sprite.png")
bird_img = pygame.transform.scale(bird_img, (bird_img.get_width() // 6, bird_img.get_height() // 6))
bird_frame = bird_img.get_rect()
bird_frame.center = (window_size[0] // 6, window_size[1] // 2)

pipe_frames = deque()
pipe_img = pygame.image.load("assets/pipe_sprite_single.png")
pipe_starting_template = pipe_img.get_rect()

# ==== Game State ====
space_between_pipes = 250
game_clock = time.time()
stage = 1
pipeSpawnTimer = 0
time_between_pipe_spawn = 40
dist_between_pipes = 500
pipe_velocity = lambda: dist_between_pipes / time_between_pipe_spawn
level = 0
score = 0
high_score = load_high_score()
didUpdateScore = False
game_is_running = True
nose_y_history = deque(maxlen=5)

# ==== Font ====
font_path = "assets/PressStart2P.ttf"
font = pygame.font.Font(font_path, 24)
font_small = pygame.font.Font(font_path, 18)
font_large = pygame.font.Font(font_path, 32)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                VID_CAP.release()
                cv.destroyAllWindows()
                pygame.quit()
                sys.exit()

        ret, frame = VID_CAP.read()
        if not ret:
            continue

        frame.flags.writeable = False
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        frame.flags.writeable = True

        screen.fill((125, 220, 232))

        if results.multi_face_landmarks:
            marker = results.multi_face_landmarks[0].landmark[94].y
            nose_y_history.append(marker)
            avg_marker = sum(nose_y_history) / len(nose_y_history)

            target_y = (avg_marker - 0.5) * 1.5 * window_size[1] + window_size[1] / 2
            max_speed = 20
            dy = target_y - bird_frame.centery
            dy = max(-max_speed, min(dy, max_speed))
            bird_frame.centery += dy

            if bird_frame.top < 0:
                bird_frame.top = 0
            if bird_frame.bottom > window_size[1]:
                bird_frame.bottom = window_size[1]

        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], 'RGB')
        screen.blit(frame_surface, (0, 0))

        for pf in pipe_frames:
            pf[0].x -= pipe_velocity()
            pf[1].x -= pipe_velocity()
        if pipe_frames and pipe_frames[0][0].right < 0:
            pipe_frames.popleft()

        screen.blit(bird_img, bird_frame)

        checker = True
        for pf in pipe_frames:
            if pf[0].left <= bird_frame.x <= pf[0].right:
                checker = False
                if not didUpdateScore:
                    score += 1
                    sound_point.play()
                    didUpdateScore = True
            screen.blit(pipe_img, pf[1])
            screen.blit(pygame.transform.flip(pipe_img, 0, 1), pf[0])
        if checker:
            didUpdateScore = False

        stage_text = font_small.render(f"Stage {stage}", True, (255, 255, 255))
        screen.blit(stage_text, (20, 20))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 50))

        pygame.display.flip()

        # ==== Collision Check ====
        if any([bird_frame.colliderect(pf[0]) or bird_frame.colliderect(pf[1]) for pf in pipe_frames]):
            sound_hit.play()
            game_is_running = False
            if score > high_score:
                high_score = score
                save_high_score(high_score)

        # ==== Game Over ====
        if not game_is_running:
            pygame.mixer.music.stop()
            sound_gameover.play()

            over_text = font_large.render("Game Over!", True, (255, 0, 0))
            try_again_text = font.render("Try Again", True, (0, 255, 0))
            exit_text = font.render("Exit", True, (0, 0, 255))
            score_display = font.render(f"Score: {score}", True, (255, 255, 255))
            high_score_display = font.render(f"High Score: {high_score}", True, (255, 255, 0))

            over_rect = over_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 60))
            try_again_rect = try_again_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 + 10))
            exit_rect = exit_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 + 70))
            score_rect = score_display.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 110))
            high_score_rect = high_score_display.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 160))

            while True:
                screen.fill((0, 0, 0))
                screen.blit(high_score_display, high_score_rect)
                screen.blit(score_display, score_rect)
                screen.blit(over_text, over_rect)
                screen.blit(try_again_text, try_again_rect)
                screen.blit(exit_text, exit_rect)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        VID_CAP.release()
                        cv.destroyAllWindows()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if try_again_rect.collidepoint(pygame.mouse.get_pos()):
                            pipe_frames.clear()
                            bird_frame.center = (window_size[0] // 6, window_size[1] // 2)
                            score = 0
                            stage = 1
                            pipeSpawnTimer = 0
                            time_between_pipe_spawn = 40
                            game_clock = time.time()
                            game_is_running = True
                            nose_y_history.clear()
                            pygame.mixer.music.play(-1)
                            sound_start.play()
                            break
                        elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                            VID_CAP.release()
                            cv.destroyAllWindows()
                            pygame.quit()
                            sys.exit()
                if game_is_running:
                    break

        # ==== Pipe Spawning ====
        if pipeSpawnTimer == 0:
            min_margin = 80
            min_gap = 120
            max_gap = 250
            dynamic_gap = random.randint(min_gap, max_gap)
            max_gap_y = window_size[1] - dynamic_gap - min_margin
            gap_y = random.randint(min_margin, max_gap_y)

            top = pipe_starting_template.copy()
            top.x = window_size[0]
            top.y = gap_y - top.height

            bottom = pipe_starting_template.copy()
            bottom.x = window_size[0]
            bottom.y = gap_y + dynamic_gap

            pipe_frames.append([top, bottom])

        pipeSpawnTimer += 1
        if pipeSpawnTimer >= time_between_pipe_spawn:
            pipeSpawnTimer = 0

        if time.time() - game_clock >= 10:
            time_between_pipe_spawn *= 5 / 6
            stage += 1
            game_clock = time.time()
