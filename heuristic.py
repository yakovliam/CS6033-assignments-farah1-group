
def heuristic(SLD):
    def h(city, goal):
        # When goal is Bucharest, this is exactly the textbook SLD
        if goal == "Bucharest":
            return SLD[city]
        # Otherwise use |SLD(city,B) - SLD(goal,B)|  (lower bound on SLD(city,goal))
        return abs(SLD[city] - SLD[goal])
    return h