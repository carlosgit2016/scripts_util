class Solution(object):
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: None Do not return anything, modify nums1 in-place instead.
        """
        t = [None] * (m+n)
        t_size = 0
        t_offset = 0
        n_offset = 0

        for i in range(m+n):
            if n == 0:
                break
            
            n1 = nums1[i]
            if i == 0:
                if (i+1) > m:
                    nums1[i] = nums2[n_offset]  
                    n_offset += 1  
                elif nums2[n_offset] < n1:
                    t[t_size] = n1
                    t_size += 1
                    nums1[i] = nums2[n_offset]
                    n_offset += 1
            elif (i+1) > m:
                if n_offset < n:
                    if (t_size - t_offset) > 0:
                        if nums2[n_offset] < t[t_offset]:
                            nums1[i] = nums2[n_offset]
                            n_offset += 1
                        else:
                            nums1[i] = t[t_offset]
                            t_offset += 1
                    else:
                        nums1[i] = nums2[n_offset]
                        n_offset += 1
                else:
                    if (t_size - t_offset) > 0:
                            nums1[i] = t[t_offset]
                            t_offset += 1        
            else:
                if n_offset < n:
                    if (t_size - t_offset) > 0:
                        if nums2[n_offset] < t[t_offset]:
                            if nums2[n_offset] < n1:
                                t[t_size] = n1
                                t_size += 1
                                nums1[i] = nums2[n_offset]
                                n_offset += 1
                        else:
                            if t[t_offset] < n1:
                                nums1[i] = t[t_offset]
                                t_offset += 1
                                t[t_size] = n1
                    else:
                        if nums2[n_offset] < n1:
                            t[t_size] = n1
                            t_size += 1
                            nums1[i] = nums2[n_offset]
                            n_offset += 1
                else:
                    if (t_size - t_offset) > 0:
                        if t[t_offset] < n1:
                            nums1[i] = t[t_offset]
                            t_offset += 1
                            t[t_size] = n1
                            t_size += 1
