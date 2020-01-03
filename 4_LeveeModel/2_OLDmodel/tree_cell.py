import random
from mesa import Agent

class TreeCell(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """
    def __init__(self, pos, model):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.timer = 0
        self.regrow_time = 3  

    def step(self, thin_burning_probability, firefighter_force):

        """
		Step function for the forest fire model
		===========================

		This function is used to advance one step forward within
		the forest fire agent based model. Each cell can perform
		one actions.
		
		"""

        self.thin_burning_probability = thin_burning_probability
        if self.thin_burning_probability > 0.010:
            print('Warning - the probability of burning of thin forests is too high! (>0.01)')
        self.thick_burning_probability = 10 * self.thin_burning_probability
        # print('Probability of burning: ' + str(self.thick_burning_probability))
        self.camp_burning_probability = 0.1
        self.firefighter_force = firefighter_force
        if self.firefighter_force >0.5:
            print('Warning - the firefigher force is too higher! (>0.5)')

        """
        If the tree is on fire, spread it to fine trees nearby.
        """

        if self.condition == "Thin forest":
            if self.timer > 3:
                self.condition = "Thick forest"
            self.timer = self.timer + 1
            if random.random() < self.thin_burning_probability:
                self.condition == "Burning"
                self.timer = 0

        if self.condition == "Thick forest":
            if random.random() < self.thick_burning_probability:
                self.condition = "Burning"

        if self.condition == "Camp site":
            if random.random() < self.camp_burning_probability:
                self.condition = "Burning"

        if self.condition =="Burnt":
            self.timer = self.timer + 1
            if self.timer > self.regrow_time:
                if random.random() < 0.5:
                    self.condition = "Thin forest"
                else:
                    self.condition = "Empty"
                self.timer = 0

        if self.condition == "Burning":
            # See if there are firefighters to extinguish the fire:
            if random.random() < self.firefighter_force:
                self.condition = "Thin forest"
            # If not, burn the neighbours depending on what they are:
            else:
                for neighbor in self.model.grid.neighbor_iter(self.pos):
                    if neighbor.condition == "Thin forest" and random.random() < 0.5:
                        neighbor.condition = "Burning"
                    if neighbor.condition == "Thick forest" and random.random() < 0.75:
                        neighbor.condition = "Burning"
                    if neighbor.condition == "Camp site":
                        neighbor.condition = "Burning"
                self.condition = "Burnt"

    def get_pos(self):
        return self.pos

    def __str__(self):
        return self.condition