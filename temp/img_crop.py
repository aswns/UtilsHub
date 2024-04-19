import os
import shutil
from PIL import Image
from math import floor
import argparse

class CropPercentage():
    """
    This class is used to crop images by a percentage of their area.
    """
    def __init__(self, probability, percentage_area, centre, randomise_percentage_area):
        """
        As well as the always required :attr:`probability` parameter, the
        constructor requires a :attr:`percentage_area` to control the area
        of the image to crop in terms of its percentage of the original image,
        and a :attr:`centre` parameter toggle whether a random area or the
        centre of the images should be cropped.

        :param probability: Controls the probability that the operation is
         performed when it is invoked in the pipeline.
        :param percentage_area: The percentage area of the original image
         to crop. A value of 0.5 would crop an area that is 50% of the area
         of the original image's size.
        :param centre: Whether to crop from the centre of the image or
         crop a random location within the image.
        :type probability: Float
        :type percentage_area: Float
        :type centre: Boolean
        """
        self.percentage_area = percentage_area
        self.centre = centre
        self.randomise_percentage_area = randomise_percentage_area

    def perform_operation(self, images, reset_center):
        """
        Crop the passed :attr:`images` by percentage area, returning the crop as an
        image.

        :param images: The image(s) to crop an area from.
        :type images: List containing PIL.Image object(s).
        :return: The transformed image(s) as a list of object(s) of type
         PIL.Image.
        """


        r_percentage_area = self.percentage_area

        # The images must be of identical size, which is checked by Pipeline.ground_truth().
        w, h = images[0].size

        w_new = int(w * r_percentage_area)
        h_new = int(h * r_percentage_area)

        def do(image):

            if reset_center:
                return image.crop((reset_center[0]-(w_new//2), reset_center[1]-(h_new//2), reset_center[0]+(w_new//2), reset_center[1]+(h_new//2)))
            else:
                return image.crop(((w//2)-(w_new//2), (h/2)-(h_new//2), (w//2)+(w_new//2), (h//2)+(h_new//2)))

        augmented_images = []

        for image in images:
            augmented_images.append(do(image))
        return augmented_images


def aug_image(aug_func):
    def wrapper(image_path, **kwargs):
        pil_img = Image.open(image_path)
        augged_img = aug_func([pil_img], **kwargs)
        return augged_img[0]

    return wrapper


@aug_image
def crop_image(images, percentage_area, reset_canter=None):
    """
    centre True center not change; False center random change
    randomise_percentage_area True means percentage_area random from [0,percentage_area]
    """

    cp_ins = CropPercentage(probability=1, percentage_area=percentage_area, centre=True,
                            randomise_percentage_area=False)
    cropped_images = cp_ins.perform_operation(images, reset_canter)

    return cropped_images



if __name__ == "__main__":


    parser = argparse.ArgumentParser("Center Crop img", add_help=True)
    parser.add_argument("--input-path", type=str, default="./images")
    parser.add_argument("--save-path", type=str, default="./cropped_images")
    parser.add_argument("--crop-ratio", type=float, default=0.5)
    args = parser.parse_args()


    percentage_area = args.crop_ratio  # 裁剪比例
    image_dir = args.input_path
    save_dir = args.save_path

    if not os.path.exists(image_dir):
        print(f"{image_dir} 不存在，请检查输入的文件地址")

    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)

    os.makedirs(save_dir)



    for image_file in os.listdir(image_dir):
        if not image_file.endswith(("bmp", "BMP", "png", "PNG", "jpg", "JPG")):
            continue
        image_path = os.path.join(image_dir, image_file)
        pil_img = Image.open(image_path)
        image_name = ".".join(image_file.split(".")[:-1])
        # crop
        cropped_img = crop_image(image_path, percentage_area=percentage_area, reset_canter=None)

        new_image_name = "{}_crop_{}.jpg".format(image_name, percentage_area)

        new_img = os.path.join(save_dir, new_image_name)
        cropped_img.save(new_img)
        print(f"cropping {image_file}")

    print(f"裁剪完成，结果已输出到cropped_images文件夹")
