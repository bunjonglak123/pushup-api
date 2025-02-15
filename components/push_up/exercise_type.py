def push_up(imlist, count, position):
    if (imlist[12][2] and imlist[11][2] >= imlist[14][2] and imlist[14][2] and imlist[13][2]):
        position = 'down'

    if (imlist[12][2] and imlist[11][2] <= imlist[14][2] and imlist[13][2] and position == 'down'):
        position = 'up'
        count += 1
        
    return count, position