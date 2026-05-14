class GameLogic:
    def __init__(self, difference_regions):
        self.difference_regions = difference_regions  # list of all diff areas from image processor
        self.found_regions = []  # store indexes of found differences
        self.remaining = len(difference_regions)  # how many still left to find
        self.mistakes = 0  # count wrong clicks
        self.max_mistakes = 3  # max allowed mistakes
        self.game_over = False  # flag to check game finished or not

    def check_click(self, x, y):
        if self.game_over:  # if already game ended
            return "game_over"

        # loop through all difference regions
        for index, (dx, dy, w, h) in enumerate(self.difference_regions):
            if index not in self.found_regions:  # check only not found ones
                # checking if click is inside this region
                if dx <= x <= dx + w and dy <= y <= dy + h:
                    self.found_regions.append(index)  # mark this region as found
                    self.remaining -= 1  # reduce remaining count

                    if self.remaining == 0:  # if all found
                        self.game_over = True
                        return "finished"

                    return "correct"  # correct click

        # if no region matched means wrong click
        self.mistakes += 1  # increase mistake count

        if self.mistakes >= self.max_mistakes:  # if exceeded limit
            self.game_over = True
            return "mistake_limit"

        return "wrong"  # just wrong but still game continues

    def get_unfound_regions(self):
        unfound = []  # list to store not found regions

        # loop all regions
        for index, region in enumerate(self.difference_regions):
            if index not in self.found_regions:  # if not found yet
                unfound.append(region)  # add to list

        return unfound  # return remaining regions
