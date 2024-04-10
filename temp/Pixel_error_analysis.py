def cal_segArea_error(pred_masks, GT_masks):
    """
    输入每张图片的分割预测mask与真实mask,输出像素误差

    Args:
        pred_masks (list): 预测分割区域的掩模列表，每个掩模是一个二维数组，表示预测分割结果
        GT_masks (list): 真实分割区域的掩模列表，每个掩模是一个二维数组，表示真实分割结果

    Returns:
        float: 像素误差
    """
    total_error = 0
    total_pixels = 0

    for pred_mask, GT_mask in zip(pred_masks, GT_masks):
        # 计算掩模的形状
        rows, cols = pred_mask.shape

        # 计算掩模之间的像素误差
        error_mask = pred_mask != GT_mask
        total_error += error_mask.sum()
        total_pixels += rows * cols

    if total_pixels == 0:
        return 0.0

    # 计算平均像素误差
    average_error = total_error / total_pixels
    return average_error

def read_yolo_ann(txt_path, img_wh, is_pred=False):
    
    pass



if __name__=="__main__":
    # 示例用法
    import numpy as np

    # 创建示例掩模
    pred_mask1 = np.array([[0, 1, 1],
                        [1, 1, 0]])
    GT_mask1 = np.array([[0, 1, 0],
                        [1, 1, 0]])

    pred_mask2 = np.array([[0, 0, 1],
                        [0, 1, 0]])
    GT_mask2 = np.array([[0, 0, 1],
                        [0, 1, 0]])

    pred_masks = [pred_mask1, pred_mask2]
    GT_masks = [GT_mask1, GT_mask2]

    error = cal_segArea_error(pred_masks, GT_masks)
    print("Segmentation area pixel error:", error)