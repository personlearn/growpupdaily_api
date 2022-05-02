from bson import ObjectId
from DB import MongoDbHelper
import os
import uuid
import configHelper


class Photo(object):
    photoformats = ['.jpg', '.jpeg', '.gif', '.png', '.bmp']

    def __init__(self):
        self.db = MongoDbHelper.MongoDbHelper('photo')
        self.url = configHelper.getConfig("photourl", "photourl")

    def getUser(self, login, pwd):
        login = self.db.getDb('login').find_one({'login': login, 'pwd': pwd})
        return {'userid': login.userid, 'url': login.url}

    def addUser(self, login, pwd, path, url):
        userid = str(uuid.uuid1()).replace('-', '')
        url = (self.url if url == '' else url)
        self.db.getDb('login').update_one({'login': login},
                                          {'$setOnInsert': {'login': login, 'pwd': pwd, 'userid': userid, 'path': path, 'url': url}}, True)
        self.initUserPhoto(userid, path, url)

    def addTagsByUserId(self, userid, tagname):
        usertags = self.db.getDb('usertags')
        usertags.update_one({'userid': userid}, {
                            '$addToSet': {'tags': tagname}}, True)

    def getTagsByUserId(self, userid):
        usertags = self.db.getDb('usertags')
        return usertags.find_one({'userid': userid})

    def addPhotoByTag(self, userid, tagids, photoid):
        phototags = self.db.getDb('phototags')
        photo = self.db.getDb('userphoto').find_one(
            {'userid': userid, '_id': ObjectId(photoid)})
        self.db.getDb('userphoto').update_one(
            {'userid': userid,'_id': ObjectId(photoid)}, {'$set':{'tagid': tagids}})

        for tagid in tagids:
            # phototags.update_one({'userid': userid, 'tagid': tagid}, {'$set':{'userid': userid, 'tagid': tagid, '$addToSet': {'photoid': ObjectId(
            #     photoid), 'photourl': photo.get('photosrc')}}}, True)
            phototags.update_one({'userid': userid, 'tagid': tagid}, { '$addToSet': {'photoid': ObjectId(
                photoid), 'photourl': photo.get('photosrc')}}, True)

        for tagid in photo.get('tagid'):
            if tagid not in tagids:
                phototags.update_one({'userid': userid, 'tagid': tagid}, {
                                     '$pull': {'photourl': photo.get('photosrc'),'photoid': photo.get('_id')}})

    def getPhotoByTag(self, userid, tagid):
        phototags = self.db.getDb('phototags')
        photoid = []
        for rest in phototags.find({'userid': userid, 'tagid': tagid}):
            photoid=photoid+rest.get('photoid')
        user = self.db.getDb('userphoto')
        result = []
        for rest in user.find({'userid': userid,'_id':{'$in':photoid}}):
            result.append(rest)
        return result

    def getAllPhoto(self, userid):
        user = self.db.getDb('userphoto')
        result = []
        for rest in user.find({'userid': userid}):
            result.append(rest)
        return result
    
    def getPhotoById(self, userid,photoid):
        user = self.db.getDb('userphoto')
        return user.find_one({'userid': userid,'_id':ObjectId(photoid)})

    def initUserPhoto(self, userid, path, url):
        lis = []
        virualpath = ''
        self.getFilesOfDir(path, virualpath, lis)
        userphotos = []
        for li in lis:
            userphotos.append({'userid': userid, 'photosrc': url+li})
        dbuserphoto = self.db.getDb('userphoto')
        dbuserphoto.insert_many(userphotos)

    def getFilesOfDir(self, path, virualpath, list_name):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                self.getFilesOfDir(file_path, virualpath+'/'+file, list_name)
            else:
                if os.path.splitext(file)[1] in self.photoformats:
                    list_name.append(virualpath+'/'+file)

    if __name__ == '__main__':
        initUserPhoto('', 'F:\漫画\灌篮高手', '')
