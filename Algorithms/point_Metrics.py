from scipy.spatial.distance import cdist
import numpy as np
import cv2


class point_Metrics:
    def center_point(point_list):
        cX = sum(point[0] for point in point_list) / len(point_list)
        cY = sum(point[1] for point in point_list) / len(point_list)
        return (cX, cY)   

    def max_pair_dist(point_list):
        """求一组二维点的最大两点之间距离[[x1,y1],[x2,y2],]

        Args:
            points_list (_type_): _description_
        """ 

        points_array = np.array(point_list)
        dist_matrix = cdist(points_array, points_array)
        max_distance = np.max(dist_matrix)
        return max_distance
    
    def min_pair_dist(point_list):
        """求一组二维点的最大两点之间距离[[x1,y1],[x2,y2],]

        Args:
            points_list (_type_): _description_
        """ 

        points_array = np.array(point_list)
        dist_matrix = cdist(points_array, points_array)
        np.fill_diagonal(dist_matrix, np.inf)  # 对角线即自身距离设置为inf
        min_distance = np.min(dist_matrix)
        return min_distance
    
    def area(point_list):
        return cv2.contourArea(point_list)


if __name__ == "__main__":
    points = [[0,0],[1,0],[0,1],[1,1]]
    print(point_Metrics.max_pair_dist(points))
    print(point_Metrics.min_pair_dist(points))