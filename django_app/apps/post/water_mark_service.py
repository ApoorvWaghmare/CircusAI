from PIL import Image
import cv2

#----------#

#======================================================================================================================#
# WatermarkService
#======================================================================================================================#

class WatermarkService:

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def add_watermark(image_path: str) -> str:
        watermark_path = '/home/ubuntu/CircusAI/application/backend/django_app/apps/post/watermark.png'
        try:
            image = Image.open(image_path)
            print('loading watermark...')
            watermark = Image.open(watermark_path)
            print('watermark loaded')
            # Desired watermark size (as a fraction of main image size)
            # For example, make watermark width be 1/10th of image width
            watermark_scale = 0.2
            new_watermark_width = int(image.size[0] * watermark_scale)
            # Calculate the new height to maintain aspect ratio
            aspect_ratio = watermark.size[1] / watermark.size[0]
            new_watermark_height = int(new_watermark_width * aspect_ratio)
            print("watermark height: ", new_watermark_height)
            print("watermark width: ", new_watermark_width)
            # Resize watermark to new dimensions
            watermark.thumbnail((new_watermark_width, new_watermark_height), Image.Resampling.LANCZOS)
            watermark.save(watermark_path)
            # Calculate the position for the watermark to be at the bottom right corner
            # Adjust these calculations if you want padding from the edges
            watermark_x = image.size[0] - watermark.size[0] - 25
            watermark_y = image.size[1] - watermark.size[1]
            print("watermark x: ", watermark_x)
            print("watermark y: ", watermark_y)
            # Paste the watermark onto the main image
            image.paste(watermark, (watermark_x, watermark_y), watermark)
            # Save the result to a new file
            image.save(image_path)
            return image_path
        except Exception as e:
            print(e)
            return ''
        
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def remove_watermark(image_path: str) -> str:
        try:
            # Load your image
            print(image_path)
            image = cv2.imread(image_path)
            print("image shape = ", image.shape)
            if (image.shape[0] != 1024) or (image.shape[1] != 1024):
                image = cv2.resize(image, (1024, 1024))
            # Specify the coordinates of the watermark area (x, y, width, height)
            # You'll need to adjust these values based on the watermark's location and size in your image
            x, y, w, h = 798, 992, 204, 32  # Example coordinates and size
            # Select the watermark area
            watermark_area = image[y : y + h, x : x + w]
            # Apply Gaussian Blur to this area
            blurred_watermark = cv2.GaussianBlur(watermark_area, (0, 0), 20)
            # Replace the original area with the blurred area
            image[y : y + h, x : x + w] = blurred_watermark
            # Save the modified image
            cv2.imwrite(image_path, image)
            return image_path
        except Exception as e:
            print(e)
            return ''
        
#======================================================================================================================#
# End of WatermarkService
#======================================================================================================================#
