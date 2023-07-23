import qrcode

def generate_qr_code(data, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

if __name__ == "__main__":
    data_to_encode = "Hello, this is a QR code generated using Python!"
    file_path = "qrcode.png"

    generate_qr_code(data_to_encode, file_path)
    print(f"QR code saved to {file_path}")
