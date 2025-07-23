from note.domain.note import Note
from note.domain.repository.note_repo import INoteRepository

class NoteRepository(INoteRepository):
    def get_notes(self, user_id, page, items_per_page):
        return super().get_notes(user_id, page, items_per_page)()
    
    def find_by_id(self, user_id, id):
        return super().find_by_id(user_id, id)
    
    def save(self, user_id, note):
        return super().save(user_id, note)
    
    def update(self, user_id, note):
        return super().update(user_id, note)
    
    def delete(self, user_id, id):
        return super().delete(user_id, id)
    
    def delete_tags(self, user_id, id):
        return super().delete_tags(user_id, id)
    
    def get_notes_by_tag_name(self, user_id, tag_name, page, items_per_page):
        return super().get_notes_by_tag_name(user_id, tag_name, page, items_per_page)