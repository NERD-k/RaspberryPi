box = (buff[1].min()-5, buff[0].min()-5, buff[1].max()+5, buff[0].max()+5)
region = image.crop(box)
regionFliter = region.filter(ImageFilter.FIND_EDGES)

