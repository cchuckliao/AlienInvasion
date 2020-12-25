import pygame.font


class Button():
    def __init__(self, ai_settings, screen, msg):
        #初始化按钮属性
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48) #None指默认字体，48是字号大小

        #创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #
        self.prep_msg(msg)

    def prep_msg(self, msg):
        # 将msg渲染为图像，并使其在按钮上居中
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) #讲存储在msg中的文本转换为图像
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect) #绘制表示按钮的矩形
        self.screen.blit(self.msg_image, self.msg_image_rect) #传递一幅画像以及与该图像相关的rect对象