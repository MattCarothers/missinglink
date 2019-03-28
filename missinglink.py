import statistics

class MissingLink():
    def __init__(self, sample_label="sample", control_label="control", minimum_control_observations=1, control_size=0):
        self.sample_label  = sample_label
        self.control_label = control_label
        self.minimum_control_observations = minimum_control_observations
        self.sample_population = {}
        self.observed_samples  = {}
        self.observed_controls = {}
        self.relationships     = {}
        self.analysis = {}
        # If the size of the control population isn't specified, it will be
        # calculated as the number of observed items that aren't explicitly
        # place in the sample group.
        self.control_size = control_size

    # Designate an item as being part of our sample population.  Anything
    # outside the sample population is assumed to be part of the control
    # population.
    def label(self, sample):
        self.sample_population[sample] = True
    
    def is_sample(self, item):
        if item in self.sample_population:
            return True
        else:
            return False

    def link(self, source, target):
        # Is this a new target?  If so, initialize the dictionaries
        if target not in self.relationships:
            self.relationships[target] = {}
            self.relationships[target][self.sample_label] = {}
            self.relationships[target][self.control_label] = {}

        # Is this source part of our sample population or part of the control
        # population?
        if self.is_sample(source):
            self.observed_samples[source] = True
            self.relationships[target][self.sample_label][source] = True
        else:
            self.observed_controls[source] = True
            self.relationships[target][self.control_label][source] = True

    @property
    def observed_target_count(self):
        return len(self.relationships.keys())
    
    @property
    def observed_sample_count(self):
        return len(self.observed_samples.keys())

    @property
    def observed_control_count(self):
        return len(self.observed_controls.keys())

    @property
    def samples(self):
        return list(self.observed_samples.keys())

    @property
    def controls(self):
        return list(self.observed_controls.keys())

    def analyze(self):
        # Total number of members of our sample population that we observed in
        # the data
        total_observed_sample_count = self.observed_sample_count
        
        # Total number of members of our control population that we observed in
        # the data
        total_observed_control_count = self.observed_control_count

        # Were we initialized with an explicit control population size?  If
        # so, use that.  Otherwise use the number of observed control set
        # members.
        if self.control_size:
            total_control_count = self.control_size
        else:
            total_control_count = total_observed_control_count

        for target in self.relationships.keys():
            # Number of members of our sample population related to this target
            observed_sample_count = len(self.relationships[target][self.sample_label].keys())
            # Number of members of our control population related to this target
            observed_control_count = len(self.relationships[target][self.control_label].keys())

            # Percent of observed sample population related to this target
            if total_observed_sample_count > 0:
                observed_sample_percent = observed_sample_count / total_observed_sample_count
            else:
                observed_sample_percent = 0
            # Percent of observed control population related to this target
            if total_control_count > 0:
                observed_control_percent = observed_control_count / total_control_count
            else:
                observed_control_percent = 0
            
            # Calculate the ratio of percentages of each population related to
            # the target.  If we did not observe any relationships from the
            # control population, use our pre-defined minimum number to avoid
            # dividing by zero.
            if observed_control_percent > 0:
                ratio = observed_sample_percent / observed_control_percent
            elif total_control_count > 0:
                artificial_observed_control_percent = self.minimum_control_observations / total_control_count
                ratio = observed_sample_percent / artificial_observed_control_percent
            else:
                ratio = 0

            self.analysis[target] = {}
            self.analysis[target]["sample_count"]  = observed_sample_count
            self.analysis[target]["control_count"] = observed_control_count
            self.analysis[target]["sample_percent"]  = observed_sample_percent
            self.analysis[target]["control_percent"] = observed_control_percent
            self.analysis[target]["ratio"] = ratio

        # Calculate the mean and standard deviation of the ratios
        self.mean  = statistics.mean([self.analysis[target]["ratio"] for target in self.analysis.keys()])
        self.stdev = statistics.pstdev([self.analysis[target]["ratio"] for target in self.analysis.keys()])

    @property
    def results(self):
        # Yield results in reverse ratio order
        for target in sorted(self.analysis.keys(), key=lambda target: self.analysis[target]["ratio"], reverse=True):
            if self.stdev != 0:
                deviations_from_mean = (self.analysis[target]["ratio"] - self.mean) / self.stdev
            else:
                deviations_from_mean = None
            yield {
                'target' : target,
                'ratio'  : self.analysis[target]["ratio"],
                'deviations_from_mean' : deviations_from_mean,
                self.sample_label + "_count"    : self.analysis[target]["sample_count"],
                self.sample_label + "_percent"  : self.analysis[target]["sample_percent"],
                self.control_label + "_count"   : self.analysis[target]["control_count"],
                self.control_label + "_percent" : self.analysis[target]["control_percent"]
            }

