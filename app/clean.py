import sqlite3

# user to index mapping in the database
user_abbr_map = {'c': 1, 'p': 2, 'b': 4}
userlist = ['unknown', 'car', 'pedestrian',
            'motorcycle', 'bicycle', 'bus', 'truck']


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

def change_user_types(db, object_id, type_as_abbr):
    """
    object_id: int, i.e. 14
    type_as_abbr: str, i.e. c, p, b for car, ped, or bike
    """
    
    object_id = int(object_id)
    type_as_abbr = type_as_abbr.lower()
    
    conn = sqlite3.connect('results.sqlite')
    cur = conn.cursor()

    queryStatement = 'UPDATE objects SET road_user_type = ? WHERE object_id = ?'
    cur.execute(queryStatement, (user_abbr_map[type_as_abbr], object_id))

    conn.commit()
    conn.close()

def delete_object(db, object_id):
    """ Removes object and its associate trajectory from the database.
    object_id: int, i.e. 14
    """
    object_id = int(object_id)

    conn = sqlite3.connect(db)
    cur = conn.cursor()
 
    #
    # Delete from objects table
    #
    queryStatement = 'DELETE FROM objects WHERE object_id = ?' 
    print queryStatement
    cur.execute(queryStatement, (object_id,))

    #
    # Extract matching trajectory_ids
    #
    queryStatement = 'SELECT * FROM objects_features WHERE object_id = ?' 
    print queryStatement
    cur.execute(queryStatement, (object_id,))

    trajectory_ids_list = []
    for row in cur:
        object_id1, trajectory_id = row
        trajectory_ids_list.append(trajectory_id)

    print trajectory_ids_list

    for trajectory_id in trajectory_ids_list:
        print "trajectory_id: ", trajectory_id
        #
        # Delete from objects_features
        #
        queryStatement = 'DELETE FROM objects_features WHERE object_id = ?' 
        cur.execute(queryStatement, (object_id,))

        #
        # Delete from positions and velocities for the object's trajectory_id
        #
        queryStatement = 'DELETE FROM positions WHERE trajectory_id = ?'
        cur.execute(queryStatement, (trajectory_id,))
        queryStatement = 'DELETE FROM velocities WHERE trajectory_id = ?'
        cur.execute(queryStatement, (trajectory_id,))
        
    # Commit once everything has been deleted
    conn.commit()

