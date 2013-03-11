import dbhandler

if __name__ == "__main__":
    db = dbhandler.DBHandler()
    r = db.look_table("settings")

    #print r

    #db.update_eigenface("sa12226224", "123")
    #print r[0]['eigenface']

    db.get_pca()
    mean, eigen = db.get_pca()
    print mean
    print eigen
    

