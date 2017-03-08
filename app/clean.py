
## Clean step
def clean(db):
    while True:
        c = execute_command(db)
        if not c:
            return

def execute_command(db):
    i = raw_input('Enter a command in the form "D12", "M6,13", or "C12,P" (D: delete, M: merge, C: change user type), or enter "q" to exit:')
    if len(i) == 0:
        print('Please enter a command')
        return True
    cmd = i[0]

    if cmd.lower() == 'q':
        return False

    args = i[1:].split(',')
    if cmd.lower() not in ['d','m','c']:
        print('Valid commands are D, M, and C')
        return True

    if cmd.lower() == 'd':
        for arg in args:
            try:
                obj = int(arg)
                print('Delete object: '+str(obj))
                delete_object(db, obj)
            except:
                print("Couldn't delete object: "+arg)

    elif cmd.lower() == 'm':
        objs_to_merge = []
        for arg in args:
            try:
                obj = int(arg)
                objs_to_merge.append(obj)
            except:
                print('Aborting, failed on object: '+arg)
                return True
        print('Merging objects: '+str(objs_to_merge))
        merge_objects(db, objs_to_merge)

    elif cmd.lower() == 'c':
        t = args[-1]
        if t.lower() not in ['c', 'b', 'p']:
            print("Can't change object to type: "+t)
            return True

        objs_to_change = []
        for j in range(len(args)-1):
            arg = args[j]
            try:
                obj = int(arg)
                objs_to_change.append(obj)
            except:
                print("Aborting, couldn't change object: "+arg)
                return True
        print("Changing objects: "+str(objs_to_change)+" to type: "+str(t))
        change_user_types(db, objs_to_change, t)

    return True

