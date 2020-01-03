from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

class ActiveAgent(Agent):
    '''
    Active agents, including policy makers, policy entrepreneurs and external parties.
    '''
    def __init__(self, pos, unique_id, model, agent_type, resources, affiliation, issuetree, policytree):
        
        '''
         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        '''
        super().__init__(unique_id, model)
        self.pos = pos  # defines the position of the agent on the grid
        self.unique_id = unique_id  # unique_id of the agent used for algorithmic reasons
        self.agent_type = agent_type  # defines the type of agents from policymaker, policyentrepreneur and externalparty
        self.resources = resources  # resources used for agents to perform actions
        self.affiliation = affiliation  # political affiliation affecting agent interactions
        self.issuetree = issuetree  # issue tree of the agent (including partial issue of other agents)
        self.policytree = policytree

        # selected issues and policies
        self.selected_PC = None
        self.selected_S = None
        self.selected_PI = None

    def selection_PC(self):

        '''
        This function is used to select the preferred policy core issue for the active agents based on all their preferences for the policy core issues.
        '''

        # compiling all the preferences
        PC_pref_list = [None for k in range(self.model.len_PC)]
        for i in range(self.model.len_PC):
            PC_pref_list[i] = self.issuetree[self.unique_id][self.model.len_DC + i][2]

        # assigning the highest preference as the selected policy core issue
        self.selected_PC = PC_pref_list.index(max(PC_pref_list))

        # print(self, self.selected_PC)
        # print("affiliation :", self.affiliation)
        # print(self.issuetree[self.unique_id][self.model.len_DC+self.selected_PC][2])
        # print(self.issuetree[self.unique_id][self.model.len_DC][2])

    # def selection_PF(self):
    #
    #     '''
    #     This function is used to select the preferred policy family. First the preferences are calculated. Then the policy family preferred is selected as the policy family with the lowest preference (this means the smallest gap after the introduction of the policy family likelihood).
    #     '''
    #
    #     len_DC = self.model.len_DC
    #     len_PF = self.model.len_PC  # number of PC is always equal to number of PF
    #     len_PC = self.model.len_PC
    #     len_S = self.model.len_S
    #
    #     # calculation of the preferences for all policy families
    #     # calculation of the denominator
    #     PF_denominator = 0
    #     # going through all policy families
    #     for PFj in range(len_PF):
    #         # going through all policy core issues
    #         for PCi in range(len_PC):
    #             gap = 0
    #             # print(" ")
    #             # print(PFj, PCi)
    #             # print(self.policytree[self.unique_id][PFj])
    #             # print(self.policytree[self.unique_id][PFj][PCi])
    #             # check if the likelihood is positive
    #             if self.policytree[self.unique_id][PFj][PCi] > 0:
    #                 # calculating the gap
    #                 # gap = self.issuetree[self.unique_id][len_DC+PCi][1] - self.issuetree[self.unique_id][len_DC+PCi][0]
    #                 # print("Before: ", gap)
    #                 gap = abs(self.issuetree[self.unique_id][len_DC+PCi][1] - (self.issuetree[self.unique_id][len_DC+PCi][0] * (1 + self.policytree[self.unique_id][PFj][PCi])))
    #                 # print("After: ", gap)
    #             # check if the likelihood is negative
    #             if self.policytree[self.unique_id][PFj][PCi] < 0:
    #                 # gap = self.issuetree[self.unique_id][len_DC+PCi][1] - self.issuetree[self.unique_id][len_DC+PCi][0]
    #                 # print("Before: ", gap)
    #                 # calculating the gap
    #                 gap = abs(self.issuetree[self.unique_id][len_DC+PCi][1] - (self.issuetree[self.unique_id][len_DC+PCi][0] * abs(self.policytree[self.unique_id][PFj][PCi])))
    #                 # print("After: ", gap)
    #             PF_denominator += round(gap,3)
    #             # print("PF_denominator: ", PF_denominator)
    #
    #     # calculation of the numerator
    #     # going through all policy families
    #     for PFj in range(len_PF):
    #         PF_numerator = 0
    #         # going through all policy core issues
    #         for PCi in range(len_PC):
    #             gap = 0
    #             # print(" ")
    #             # print(PFj, PCi)
    #             # print(self.policytree[self.unique_id][PFj])
    #             # print(self.policytree[self.unique_id][PFj][PCi])
    #             # check if the likelihood is positive
    #             if self.policytree[self.unique_id][PFj][PCi] > 0:
    #                 # calculating the gap
    #                 # gap = self.issuetree[self.unique_id][len_DC+PCi][1] - self.issuetree[self.unique_id][len_DC+PCi][0]
    #                 # print("Before: ", gap)
    #                 gap = abs(self.issuetree[self.unique_id][len_DC+PCi][1] - (self.issuetree[self.unique_id][len_DC+PCi][0] * (1 + self.policytree[self.unique_id][PFj][PCi])))
    #                 # print("After: ", gap)
    #             # check if the likelihood is negative
    #             if self.policytree[self.unique_id][PFj][PCi] < 0:
    #                 # gap = self.issuetree[self.unique_id][len_DC+PCi][1] - self.issuetree[self.unique_id][len_DC+PCi][0]
    #                 # print("Before: ", gap)
    #                 # calculating the gap
    #                 gap = abs(self.issuetree[self.unique_id][len_DC+PCi][1] - (self.issuetree[self.unique_id][len_DC+PCi][0] * abs(self.policytree[self.unique_id][PFj][PCi])))
    #                 # print("After: ", gap)
    #             PF_numerator += round(gap,3)
    #         self.policytree[self.unique_id][PFj][len_PC] = round(PF_numerator/PF_denominator,3)
    #     #     print(self.issuetree[self.unique_id][PFj])
    #     # print(self.issuetree[self.unique_id])
    #
    #     # selection of the preferred policy family
    #     # compiling all the preferences
    #     PF_pref_list = [None for k in range(len_PC)]
    #     for i in range(len_PC):
    #         PF_pref_list[i] = self.policytree[self.unique_id][i][len_PC]
    #
    #     # assigning the lowest preference as the selected policy family by the agent
    #     self.selected_PF = PF_pref_list.index(min(PF_pref_list))

    def selection_S(self):

        '''
        This function is used to select the preferred secondary issue. First, only the secondary issues that are related, through a causal relation, to the policy core issue on the agenda are placed into an array. Then, the one with the highest preference is selected. It is then used as the issue that the agent will advocate for later on.
        '''

        len_DC = self.model.len_DC
        len_PC = self.model.len_PC
        len_S = self.model.len_S

        # considering only issues related to the issue on the agenda
        S_pref_list_indices = []
        for i in range(len_S):
            if self.issuetree[self.unique_id][len_DC+len_PC+len_S+len_DC*len_PC+self.model.agenda_PC*len_S+i][0] !=0:
                S_pref_list_indices.append(i)

        S_pref_list = [None for i in range(len(S_pref_list_indices))]
        for i in range(len(S_pref_list)):
            S_pref_list[i] = self.issuetree[self.unique_id][len_DC+len_PC+S_pref_list_indices[i]][2]

        # assigning the highest preference as the selected policy core issue
        self.selected_S = S_pref_list.index(max(S_pref_list))
        # make sure to select the right value in the list of indices (and not based on the index in the list of preferences)
        self.selected_S = S_pref_list_indices[self.selected_S]

        # print(self, self.selected_S)
        # print("affiliation :", self.affiliation)
        # print(self.issuetree[self.unique_id][len_DC+len_PC+self.selected_S][2])
        # print(self.issuetree[self.unique_id])

    def selection_PI(self):
        
        '''
        This function is used to select the preferred policy instrument from the policy family on the agenda. First the preferences are calculated. Then the policy family preferred is selected as the policy family with the lowest preference (this means the smallest gap after the introduction of the policy family likelihood).

        Note that the algorithm considers the PF version where the policy family selected is the one for containing all policy instruments - as policy families are not implemented in this version of the model. This is to avoid having to rewrite the entire code.
        '''


        len_DC = self.model.len_DC
        len_PF = self.model.len_PC  # number of PC is always equal to number of PF
        len_PC = self.model.len_PC
        len_S = self.model.len_S

        # selecting the policy instrument from the policy family on the agenda
        PFIns_indices = self.model.PF_indices[self.model.agenda_PF]

        # calculation of the preferences for all policy instruments
        # calculation of the denominator
        PI_denominator = 0
        # going through all policy instruments
        for PIj in range(len(PFIns_indices)):
            # going through all secondary issues
            for Si in range(len_S):
                # print(" ")
                # print(PIj, Si)
                # print(self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]])
                # print(self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si])
                # check if the likelihood is positive
                gap = 0
                if self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si] > 0:
                    # calculating the gap
                    # gap = self.issuetree[self.unique_id][len_DC+len_PC+Si][1] - self.issuetree[self.unique_id][len_DC+len_PC+Si][0]
                    # print("Before: ", self.issuetree[self.unique_id][len_DC+len_PC+Si][1] - self.issuetree[self.unique_id][len_DC+len_PC+Si][0], self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si])
                    gap = abs(self.issuetree[self.unique_id][len_DC+len_PC+Si][1] - (self.issuetree[self.unique_id][len_DC+len_PC+Si][0] * (1 + self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si])))
                    # print("After: ", gap)
                # check if the likelihood is negative
                if self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si] < 0:
                    # gap = self.issuetree[self.unique_id][len_DC+len_PC+Si][1] - self.issuetree[self.unique_id][len_DC+len_PC+Si][0]
                    # print("Before: ", self.issuetree[self.unique_id][len_DC+len_PC+Si][1] - self.issuetree[self.unique_id][len_DC+len_PC+Si][0], self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si])
                    # calculating the gap
                    gap = abs(self.issuetree[self.unique_id][len_DC+len_PC+Si][1] - (self.issuetree[self.unique_id][len_DC+len_PC+Si][0] * abs(self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si])))
                    # print("After: ", gap)
                PI_denominator += round(gap,3)
                # print("PI_denominator: ", PI_denominator)

        # calculation of the numerator
        # going through all policy instruments
        for PIj in range(len(PFIns_indices)):
            PI_numerator = 0
            # going through all secondary issues
            for Si in range(len_S):
                # print(" ")
                # print(PIj, Si)
                # print(self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]])
                # print(self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si])
                # check if the impact is positive
                if self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si] > 0:
                    # calculating the gap
                    # gap = self.issuetree[self.unique_id][len_DC+len_PC+Si][1] - self.issuetree[self.unique_id][len_DC+len_PC+Si][0]
                    # print("Before: ", gap)
                    gap = abs(self.issuetree[self.unique_id][len_DC+len_PC+Si][1] - (self.issuetree[self.unique_id][len_DC+len_PC+Si][0] * (1 + self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si])))
                    # print("After: ", gap)
                # check if the likelihood is negative
                if self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si] < 0:
                    # gap = self.issuetree[self.unique_id][len_DC+len_PC+Si][1] - self.issuetree[self.unique_id][len_DC+len_PC+Si][0]
                    # print("Before: ", gap)
                    # calculating the gap
                    gap = abs(self.issuetree[self.unique_id][len_DC+len_PC+Si][1] - (self.issuetree[self.unique_id][len_DC+len_PC+Si][0] * abs(self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][Si])))
                    # print("After: ", gap)
                PI_numerator += round(gap,3)
            self.policytree[self.unique_id][len_PF + PFIns_indices[PIj]][len_S] = round(PI_numerator/PI_denominator,3)
            # print(self.issuetree[self.unique_id][PFj])
        # print(self.policytree[self.unique_id])

        # selection of the preferred policy instrument
        # compiling all the preferences
        PI_pref_list = [None for k in range(len(PFIns_indices))]
        for i in range(len(PFIns_indices)):
            PI_pref_list[i] = self.policytree[self.unique_id][len_PF + PFIns_indices[i]][len_S]

        # assigning the lowest preference as the selected policy instrument by the agent
        self.selected_PI = PI_pref_list.index(min(PI_pref_list))
        # print("Index chosen from PFX: ", self.selected_PI)
        # print("self.model.PF_indices", self.model.PF_indices[self.model.agenda_PF])
        self.selected_PI = self.model.PF_indices[self.model.agenda_PF][self.selected_PI]
        # print("Policy instrument selected: ",self.selected_PI)


class ElectorateAgent(Agent):
    '''
    Electorate agents.
    '''
    def __init__(self, pos, unique_id, model, affiliation, issuetree_elec, representativeness):
        '''
         Create a new Electorate agent.
         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            unique_id: 
        '''
        super().__init__(pos, model)
        self.pos = pos  # defines the position of the agent on the grid
        self.unique_id = unique_id  # unique_id of the agent used for algorithmic reasons
        self.affiliation = affiliation  # political affiliation affecting agent interactions
        self.issuetree_elec = issuetree_elec  # issue tree of the agent (including partial issue of other agents)
        self.representativeness = representativeness


    def electorate_influence(self, w_el_influence):

        '''
        Function that defines the electorate influence on the policy makers.
        This function is dependent on the electorate influence weight value which can be adjusted as a tuning parameter.
        '''

        len_DC = self.model.len_DC
        len_PC = self.model.len_PC
        len_S = self.model.len_S

        for agent in self.model.schedule.agent_buffer(shuffled=True):
            if isinstance(agent, ActiveAgent) and agent.agent_type == 'policymaker' and agent.affiliation == self.affiliation:
                # print(' ')
                # print('Before', agent.issuetree[agent.unique_id])
                _unique_id = agent.unique_id
                for issue in range(len_DC+len_PC+len_S):
                    agent.issuetree[_unique_id][issue][1] += (self.issuetree_elec[issue] - agent.issuetree[_unique_id][issue][1]) * w_el_influence * abs(agent.issuetree[_unique_id][issue][1] - agent.issuetree[_unique_id][issue][0])
                # print('After', agent.issuetree[agent.unique_id])

class TruthAgent(Agent):
    '''
    Truth agents.
    '''
    def __init__(self, pos, model, issuetree_truth, policytree_truth):
        '''
         Create a new Truth agent.
         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
        '''
        super().__init__(pos, model)
        self.pos = pos  # defines the position of the agent on the grid
        self.issuetree_truth = issuetree_truth  # issue tree of the agent (including partial issue of other agents)
        self.policytree_truth = policytree_truth
    