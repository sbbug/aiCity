import matplotlib.pyplot as plt

# 显示高度
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.- 0.2, 1.03*height, '%s' % int(height))


name_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
num_list = [33, 44, 53, 16, 11, 17, 17, 10]
autolabel(plt.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list))
plt.savefig("temp.jpg")
#plt.show()

