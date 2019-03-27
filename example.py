#!/usr/bin/env python3

import json
from missinglink import MissingLink

if __name__ == "__main__":
    # Create a new MissingLink object with the sample and control groups
    # labeled "infected" and "clean."  The labels are optional.  Default
    # labels are "sample" and "control."
    linker = MissingLink("infected", "clean")
    # Designate some entities as being part of the sample group.  Everything
    # else is assumed to be part of the control group.  These are our
    # infected IPs:
    linker.label("10.0.0.1")
    linker.label("10.0.0.2")
    linker.label("10.0.0.3")

    # Add relationships
    # 6.6.6.6 is our ficticous malicious IP.  Two of our infected IPs have
    # connected to it.
    linker.link("10.0.0.1", "6.6.6.6")
    linker.link("10.0.0.2", "6.6.6.6")

    # 8.8.8.8 is a benign IP.  All our sample and control IPs have connected
    # to it.
    linker.link("10.0.0.1", "8.8.8.8")
    linker.link("10.0.0.2", "8.8.8.8")
    linker.link("10.0.0.3", "8.8.8.8")
    linker.link("10.0.0.4", "8.8.8.8")
    linker.link("10.0.0.5", "8.8.8.8")
    linker.link("10.0.0.6", "8.8.8.8")
    
    # 9.9.9.9 is another benign IP.  One of our control IPs connected to
    # it.
    linker.link("10.0.0.6", "9.9.9.9")

    # Analyze the results
    linker.analyze()
    print("Number of entities in the sample group:",
            linker.observed_sample_count)
    print("Number of entities in the control group:", 
            linker.observed_control_count)
    print("Members of the sample group:", linker.samples)
    print("Members of the control group:", linker.controls)
    print("Analysis results:")
    for result in linker.results:
        print(json.dumps(result))
