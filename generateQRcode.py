import qrcode

# 你的网站URL
url = "https://mcleolee.wordpress.com"

# 生成二维码
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# 创建图像
img = qr.make_image(fill="black", back_color="white")

# 保存二维码
img.save("mcleolee_qr.png")

# 显示二维码
img.show()
