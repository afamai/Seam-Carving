from skimage import filters, color
import numpy as np
cimport cython
cimport numpy as np
import time
DTYPE = np.int_
ctypedef np.int_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def compute_scoring_matrix(int[:, :, :] image):
    # computer the energy image using gradient magnitude
    start = time.time()
    cdef np.ndarray matrix = filters.sobel(color.rgb2gray(image))
    start = time.time()
    cdef int r = matrix.shape[0]
    cdef int c = matrix.shape[1]
    cdef int i, j
    for i in range(1, r):
        for j in range(c):
            if j == 0:
                matrix[i, j] += min(matrix[i-1, j], matrix[i-1, j+1])
            elif j == c-1:
                matrix[i, j] += min(matrix[i-1, j-1], matrix[i-1, j])
            else:
                matrix[i, j] += min(matrix[i-1, j-1], matrix[i-1, j], matrix[i-1, j+1])
    return matrix

def minimum_seam(matrix):
    r, c = matrix.shape
    # mask = np.ones((r, c), dtype=np.bool)
    mask = []
    for i in reversed(range(r)):
        if i == r-1:
            j = np.argmin(matrix[-1])
        else:
            if j == 0:
                j += np.argmin(matrix[i, j:j+2])
            else:
                j += np.argmin(matrix[i, j-1:j+2]) - 1
        # mask[i, j] = False
        mask.append(i * c + j)
    return mask

def remove_seams(image, amount):
    img = image.copy()
    for _ in range(amount):
        score_matrix = compute_scoring_matrix(img)
        seam = minimum_seam(score_matrix)

        # remove seam from image
        r, c, _ = img.shape
        # img = img[mask].reshape((r, c-1, 3))
        img = np.delete(img.reshape((r*c, 3)), seam, axis=0).reshape((r, c-1, 3))
    
    return img

def add_seams(image, amount):
    img = image.copy()
    seam_record = []
    
    # remove seams to determine the optimal seams to duplicate
    for _ in range(amount):
        score_matrix = compute_scoring_matrix(img)
        seam = minimum_seam(score_matrix)
        # store the seam for insertion later
        seam_record.append(seam)
        # remove seam from image
        r, c, _ = img.shape
        img = np.delete(img.reshape((r*c, 3)), seam, axis=0).reshape((r, c-1, 3))

    # insert seams
    img = image.copy()
    seams_inserted = []
    for i, seam in enumerate(seam_record):
        # get the col position of the first pixel from the top of the seam
        col = seam[-1]
        # use binary search to determine how many seams were inserted before this one
        offset = insertSearch(seams_inserted, col)
        seams_inserted.insert(offset, col+offset)

        # insert the seam by duplicating the pixels along the seam
        r, c, _ = img.shape
        temp = np.zeros((r, c+1, 3))
        for j, p in enumerate(seam):
            row = r-j-1
            col = p - (row * (c-i*2)) + offset*2
            if col == 0:
                # if pixel is on the left edge then duplicate pixel without averaging color
                temp[row, col] = img[row, col]
                temp[row, col+1:] = img[row, col:]
            else:
                # otherwise, duplicate a new pixel with the average color between the left and right pixels
                temp[row, :col] = img[row, :col]
                temp[row, col] = np.round((img[row, col-1] + img[row, col])/2)
                temp[row, col+1:] = img[row, col:]
        img = temp
    return img.astype(np.int_)


def insertSearch(arr, val):
    low = 0
    high = len(arr) - 1

    while (low <= high):
        mid = int(low + (high - low)/2)
        if (arr[mid] > val):
            high = mid-1
        else:
            low = mid+1
    
    return low
