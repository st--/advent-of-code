import numpy as np
nums = np.loadtxt("1.txt").astype(int)
for idx in np.where(nums[:, None] + nums[None, :] == 2020):
    x = nums[idx]
    print(np.prod(x))
for idx in np.where(nums[:, None, None] + nums[None, :, None] + nums[None, None, :] == 2020):
    print(np.prod([nums[i] for i in set(idx)]))
