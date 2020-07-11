import time
import numpy as np
from matplotlib import pyplot as plt

def calc_slope(left, right):
    """
    Calculates the slope between two point in R2

    Temporal Complexity:
        3 operations => O(1)

    Parameters:
        left (tuple) left point
        right (tuple) right point
    Returns: 
        slope (float) slope between the two points
    """
    return (left[1] - right[1]) / (left[0] - right[0])

def combine_hulls(left, right, side, left_most, right_most):
    """
    Given a left and right convex hull, compute and return the 
    set of points that form a combined convex hull

    Temporal Complexity:
        O(p(n+m)) where p is max(n,m) (See comments below for details)

    Spacial Complextiy:
        3 + 7 (first while) + 3 + 7 (second while) + n+m+2 (result list)
        Thus total of n+m+22 = O(n+m)

    Parameters:
        left ((n,) list) list of left subhull ordered in counter-clockwise
                    orientation starting with the right most point
        right ((m,) list) list of right subhull ordered in clockwise
                    orientation starting with the left most point
        side (str) which side the two sublists came from, right left or None 
                    where None means it is the last combination
        left_most (int) index of the right most index (spacially) in the left list
        right_most (int) index of the left most index (spacialy) in the right list
    """
    upper_left = 0
    upper_right = 0
    updated = True

    # Worst case this while loop runs max(n, m) times if each hull is an arc
    # i.e. O(n(n+m)) or O(m(n+m)) 
    while updated:
        # Worst case 5(n-1 + m-1) + 6 => O(n+m)
        updated = False

        # 3 operations in calc_slope
        left_slope = calc_slope(left[upper_left], right[upper_right])
        init_upper_left = upper_left

        # 5(n-1) => O(n)
        for i in range(init_upper_left+1, len(left)):
            # 3 operations in calc_slope
            left_new_slope = calc_slope(left[i], right[upper_right])

            # Max 2 operations 
            if left_new_slope > left_slope:
                upper_left = i - 1
                break
            else:
                updated = True
                upper_left = i
                left_slope = left_new_slope

        # 3 operations in calc_slope
        right_slope = calc_slope(left[upper_left], right[upper_right])
        init_upper_right = upper_right

        # 5(m-1) => O(m)
        for i in range(init_upper_right+1, len(right)):
            # 3 operations in calc_slope
            right_new_slope = calc_slope(left[upper_left], right[i])

            # Max 2 operations
            if right_new_slope < right_slope:
                upper_right = i - 1
                break
            else:
                updated = True
                upper_right = i
                right_slope = right_new_slope
    
    # Calculate lower common tangent
    lower_left = 0
    lower_right = 0
    updated = True

    # Same as last while loop => O(n(n+m)) or O(m(n+m)) 
    while updated:
        updated = False
        left_slope = calc_slope(left[-lower_left], right[-lower_right])
        init_lower_left = lower_left
        for i in range(init_lower_left+1, len(left)):
            left_new_slope = calc_slope(left[-i], right[-lower_right])
            if left_new_slope < left_slope:
                lower_left = i - 1
                break
            else:
                updated = True
                lower_left = i
                left_slope = left_new_slope
        
        right_slope = calc_slope(left[-lower_left], right[-lower_right])
        init_lower_right = lower_right
        for i in range(init_lower_right+1, len(right)):
            right_new_slope = calc_slope(left[-lower_left], right[-i])
            if right_new_slope > right_slope:
                lower_right = i - 1
                break
            else:
                updated = True
                lower_right = i
                right_slope = right_new_slope

    # Since lower tangents are found in the backwards orientation, adjust them back
    # to the index in the correct orientation
    # Max of 4 operations
    if lower_left != 0:
        lower_left = len(left) - lower_left
    if lower_right != 0:
        lower_right = len(right) - lower_right

    # Sort right hulls clockwise, left counter-clockwise
    result = []
    # Total temportal complexity for the right side is
    # n+m+n+m+n = 3n + 2m => O(n+m)
    if side == "r":
        # list.extend is O(k) where k are number of elements added
        # thus worst case senario is O(n+m)
        # Reversing the lists ([::-1]) is also O(k) and is worst case
        # Applied to the whole left hull, this O(n)
        result.extend(left[upper_left:left_most+1][::-1])
        if upper_right > lower_right:
            result.extend(right[upper_right:])
            result.extend(right[:lower_right+1])
        else:    
            result.extend(right[upper_right:lower_right+1])

        # Index function is O(l) (l is length of result at this point)
        # Worst case is O(n+m) if all of left and right are in result
        new_right_most = np.argmax([result[i][0] for i in range(len(result))])
        
        if lower_left != left_most:
            if lower_left > upper_left:
                result.extend(left[left_most+1:lower_left+1][::-1])
            else:
                result.extend(left[:lower_left+1][::-1])
                result.extend(left[left_most+1:][::-1])
    # Temporal complexity of left sides is 3m + 2n = O(m+n) similarly
    # If side is None, default to counter-clockwise
    else:
        result.extend(right[upper_right:right_most+1][::-1])
        if upper_left > lower_left: 
            result.extend(left[upper_left:])
            result.extend(left[:lower_left+1][::-1])
        else:
            result.extend(left[upper_left:lower_left+1])

        new_left_most = np.argmin([result[i][0] for i in range(len(result))])

        if lower_right != right_most:
            if lower_right > upper_right:
                result.extend(right[right_most+1:lower_right+1][::-1])
            else:
                result.extend(right[:lower_right+1][::-1])
                result.extend(right[right_most+1:][::-1])
    if side == "r":
        return result, new_right_most
    else:
        return result, new_left_most

def recursive_hull(sublist, side):
        """
        Function that recursively divides the problem into 2 sides

        Temporal Complexity:
            Divides problem into 2 subproblems of size (n)/2 with O(n^2). 
            Assuming without loss of generality that p = n, by the Master's 
            Theorem with a=2, b=2 and d=2 we have O(n^2).

        Spacial Complexity:
            1 + 1 + n/2 + n/2 + 2 + n/2 + n/2 + n (combine hulls call) => O(n)
            spacial complexity for each call. 

        Parameters:
            sublist (list) list of points 
            side (str) "l" or "r" side points are on, left are ordered
                        counter-clockwise from right most point, right 
                        are ordered clockwise from left most point
        """
        m = len(sublist)
        # Base case
        # Order left list counter-clockwise from right most
        if  side == "l":
            if m == 2:
                return sublist[::-1], 1
            elif m == 3:
                first_slope = calc_slope(sublist[0], sublist[1])
                second_slope = calc_slope(sublist[0], sublist[2])
                if first_slope > second_slope:
                    return sublist[::-1], 2
                else:
                    return [sublist[2], sublist[0], sublist[1]], 1
        else: # Order right list clockwise from left most
            if m == 2:
                return sublist, 1
            elif m == 3:
                first_slope = calc_slope(sublist[0], sublist[1])
                second_slope = calc_slope(sublist[0], sublist[2])
                if first_slope > second_slope:
                    return sublist, 2
                else:
                    return [sublist[0], sublist[2], sublist[1]], 1

        mid = m // 2
        left, right = sublist[:mid], sublist[mid:]
        l_hull, left_most = recursive_hull(left, "l") 
        r_hull, right_most = recursive_hull(right, "r")
        
        return combine_hulls(l_hull, r_hull, side, left_most, right_most)

def empirical_analysis():
    ns = [10, 100, 1_000, 10_000, 100_000, 500_000, 1_000_000]
    mean_times = []
    all_times = []
    for n in ns:
        all_times.append(n)
        draws = []
        for _ in range(5):
            # random angle
            alpha = 2 * np.pi * np.random.random(n)
            # random radius
            r = np.sqrt(np.random.random(n))
            # calculating coordinates
            x = r * np.cos(alpha)
            y = r * np.sin(alpha)
            points = list(zip(x,y))
            draws.append(points)
        
        times = []
        for points_list in draws:
            print(n)
            # print(points_list)
            start = time.time()
            mid = len(points_list) // 2
            left, right = points_list[:mid], points_list[mid:]
            # print("Left", left)
            # print()
            # print("Right", right)
            # print()
            left, left_most = recursive_hull(left, "l")
            right, right_most = recursive_hull(right, "r")

            # print(left_most, right_most)
            # print()

            combine_hulls(left, right, None, left_most, right_most)
            end = time.time() - start
            times.append(end)
            all_times.append(end)
        mean_times.append(np.mean(times))

    plt.loglog(ns, mean_times)
    plt.xlabel("Number of points")
    plt.xscale("log")
    plt.ylabel("Time (seconds)")
    plt.title("Complexity of Convex Hull")
    plt.show()

    print(mean_times)
    print()
    print(all_times)

    return mean_times, all_times