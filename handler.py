from Markov import *

#cloud_function(platforms=[Platform.AWS], memory=512, config=config)
def yourFunction(request, context):
    import json
    import logging
    from Inspector import Inspector
    import time
    
    # Import the module and collect data 
    inspector = Inspector()
    inspector.inspectAll()

    # Add custom message and finish the function
    if ('words' in request):
        word_list = str(request['words']).split(" ")
        fill_master_dict(word_list)
        story_sequence = generate_story()
        inspector.addAttribute("message", stringify_story(story_sequence))
    else:
        inspector.addAttribute("message", "ERROR: Improper Input Provided")
    
    inspector.inspectAllDeltas()
    return inspector.finish()
