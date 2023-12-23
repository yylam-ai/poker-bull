import random

"""
POKER BULL:
The game employs a standard deck of cards, excluding jokers. Each card's point value is determined by its displayed number, with Aces valued at 1 point, and the face cards (J, Q, K) each worth 10 points.

In this game, players are dealt five cards, and an intriguing twist allows the card '6' to be considered as '3,' and vice versa. 
The key aspect of the game revolves around the concept of 'Niu,' where players strategically select three cards, summing their point values. 
If the total is a multiple of 10, the player's hand point total is then determined by the remaining two cards. 
For instance, if the sum of three cards is 20, the total of the remaining two cards, when taken modulo 11, becomes the player's final score. 
The scoring system ranges from 1 (lowest) to 10 (highest).

Players engage in friendly competition by comparing their point totals, and the participant with the highest score emerges victorious. 
Notably, there are special scenarios where the remaining two cards form a pair or a specific combination, such as a picture card paired with an Ace of Spades, leading to unique winning outcomes with varied rewards.

In summary:
Picture card + Ace of Spades > Pair > Regular Score"""

class PokerBullGame:
    def __init__(self):
        self.card_num_dict = {
            "A": 1,
            "Aa": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 10,
            "Q": 10,
            "K": 10
        }

        self.picture = ["J", "Q", "K"]

    def nums_to_hand(self, hand, nums):
        converted_hand = [hand[num] for num in nums]
        return converted_hand

    def find_10(self, ori_hand):
      # Lists to store combinations of three cards and corresponding points
      trip = []
      trip_check = []
      points = []
      scores = []
      hand = ori_hand.copy()

      # Get the original indices of cards in the hand before sorting
      orig_idx = [i[0] for i in sorted(enumerate(hand), key=lambda x:x[1])]

      # Sort the hand in ascending order
      hand.sort()

      # Iterate through each card in the hand
      for i in range(len(hand)):
        # Initialize pointers for the two ends of the hand
        left = i+1
        right = len(hand)-1

        # Calculate the target sum for a pair of cards
        target = 10 - hand[i]

        # Store the value of the current card
        prev = hand[i] 

        # Loop until the left and right pointers meet
        while left < right:
          # Create copies of the hand and indices to avoid modifying the original lists
          dup = hand.copy()
          idx_dup = orig_idx.copy()

          # Check if the current combination is not valid, adjust pointers accordingly
          if ((dup[left] + dup[right]) % 10 > target or (dup[left] + dup[right]) % 10 == 0) and (dup[left] + dup[right]) % 10 != target:
            right -= 1
          elif (dup[left] + dup[right]) % 10 < target:
            # If the sum is less than the target, adjust left pointer and check for additional conditions
            if dup[right]==10 and target not in dup:
              right -=1
            else:
              prev = hand[left]
              left += 1
            # Check if the updated left pointer forms a valid combination with the previous card
            if left > 1 and dup[left] + prev == target:
              right = left
              left -=1

          else:
            # Check if the combination is not already in the 'trip' list
            if [idx_dup[right],idx_dup[left],idx_dup[i]] not in trip:
              # Add the combination to the 'trip' list and corresponding points to 'points'
              trip.append([idx_dup.pop(right),idx_dup.pop(left),idx_dup.pop(i)])
              p1, p2 = idx_dup.pop(),idx_dup.pop()
              points.append([p1,p2])
              scores.append([ori_hand[p1], ori_hand[p2]])

            prev = hand[left]
            left += 1
              
      # Return the indexes of the lists of combinations, corresponding valid index for points calculation, and the point of each valid index respectively
      return trip, points, scores

    def find_3_6(self, nums, comb):
      for i in range(len(nums)):
        if nums[i] == 3 or nums[i] ==6:
          trans = (nums[i]*2) % 9 # change 3 to 6, 6 to 3
          new = nums[:i] + [trans] + nums[i+1:]

          if new not in comb:
            comb.append(new)
            self.find_3_6(comb[-1], comb)

    def poker_bull(self, hand, nums):
        trip, points, scores = [], [], []

        for num in nums:
            under, upper, score = self.find_10(num)

            for i in range(len(upper)):
                under_cards = self.nums_to_hand(hand, under[i])
                upper_cards = self.nums_to_hand(hand, upper[i])
                # score = self.card_num_dict[upper_cards[0]] + self.card_num_dict[upper_cards[1]]
                scores.append(sum(score[i]))
                trip.append(under_cards)
                points.append(upper_cards)

        return trip, points, scores

    def play_game(self):
        cards_list = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4
        cards_list[0] = "Aa"  # replace one of the aces with the ace of spade

        hand = []
        nums = []
        result = []

        for i in range(5):
            random_num = random.randint(0, 4 * (len(self.card_num_dict) - 1) - 1 - i)
            hand.append(cards_list.pop(random_num))

        nums = [self.card_num_dict[i] for i in hand]  # convert hand to numbers
        comb = [nums.copy()]
        self.find_3_6(nums, comb)  # expand all possible combinations when 3s are converted to 6s, and 6s are converted to 3s

        print("Hand:", hand)

        trip, points, scores = self.poker_bull(hand, comb)

        for i in range(len(points)):
            if points[i][0] == points[i][1]:
                result.append("pair!, 3x winning")
            elif (points[i][0] == "Aa" and points[i][1] in self.picture) or (
                    points[i][1] == "Aa" and points[i][0] in self.picture):
                result.append("Cow + water!, 5x winning")
            elif points[i][0] in self.picture and points[i][1] in self.picture and sum(
                    [t in self.picture for t in trip[i]]) == 3:
                result.append("5 Picture!, 7x winning")
            else:
                total = scores[i] % 10
                if total != 0:
                    result.append("{} points!, 1x winning".format(total))
                else:
                    result.append("{} points!, 2x winning".format(10))

        if trip:
          print("The possible winning combinations are:")
          for i in range(len(trip)):
              print("Under:{}, upper:{}, result: {}".format(trip[i], points[i], result[i]))
        else:
            print("0 points")


poker_game = PokerBullGame()
poker_game.play_game()
