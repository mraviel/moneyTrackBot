import models as M
from datetime import datetime
from sqlalchemy import extract


class DatabaseCommands:

    def __init__(self, db):
        self.db = db

    @staticmethod
    def get_register_request_exists(author_id):
        return M.RegisterRequest.query.filter_by(author_id=author_id).first()

    @staticmethod
    def get_register_request_by_id(register_id):
        return M.RegisterRequest.query.filter_by(register_id=register_id)

    @staticmethod
    def get_all_register_requests():
        return M.RegisterRequest.query.all()

    @staticmethod
    def get_user_exists(author_id):
        return M.Users.query.filter_by(author_id=author_id).first()

    @staticmethod
    def get_all_users():
        return M.Users.query.all()

    @staticmethod
    def get_all_subjects(author_id):
        return M.Subjects.query.filter_by(author_id=author_id).all()

    @staticmethod
    def get_all_expenses(author_id):
        return M.Messages.query.filter_by(author_id=author_id, is_expense=True).all()

    @staticmethod
    def get_all_income(author_id):
        return M.Messages.query.filter_by(author_id=author_id, is_expense=False).all()

    def get_this_month_expenses(self, author_id):
        return self.db.session.query(M.Messages).filter(M.Messages.author_id == author_id,
                                                        M.Messages.is_expense == True,
                                                        extract('month', M.Messages.message_datetime) >= datetime.today().month,
                                                        extract('year', M.Messages.message_datetime) >= datetime.today().year
                                                        ).all()

    def get_this_month_income(self, author_id):
        return self.db.session.query(M.Messages).filter(M.Messages.author_id == author_id,
                                                        M.Messages.is_expense == False,
                                                        extract('month', M.Messages.message_datetime) >= datetime.today().month,
                                                        extract('year', M.Messages.message_datetime) >= datetime.today().year
                                                        ).all()

    def add_register_request(self, author_details):
        """ Add register request """
        register_request = M.RegisterRequest(author_id=author_details['id'], first_name=author_details['first_name'],
                                             last_name=author_details['last_name'],
                                             is_bot=author_details['is_bot'],
                                             language_code=author_details['language_code'])

        self.db.session.add(register_request)
        self.db.session.commit()

    def remove_register_request(self, register_id):
        """ Remove register request from db """
        register_obj = M.RegisterRequest.query.filter_by(register_id=register_id).first()

        # Delete
        if register_obj:
            delete_subject = self.db.session.get(M.RegisterRequest, register_obj.register_id)
            self.db.session.delete(delete_subject)
            self.db.session.commit()
            return True

    def add_user(self, author_details):
        """ Add new user to db """
        User = M.Users(author_id=author_details.author_id, first_name=author_details.first_name,
                       last_name=author_details.last_name,
                       is_bot=author_details.is_bot, language_code=author_details.language_code)

        self.db.session.add(User)
        self.db.session.commit()

    def delete_user(self, author_id):
        """ Delete user """
        pass

    def add_subject(self, main_subject, author_id):
        """ Add new subject to db"""
        # Check if subject already exists for the user
        current_subjects = self.get_all_subjects(author_id)
        for subject in current_subjects:
            if main_subject == subject.subjects_title:
                # If None
                return

        new_subject = M.Subjects(author_id=author_id, subjects_title=main_subject)
        self.db.session.add(new_subject)
        self.db.session.commit()

    def delete_subject(self, main_subject, author_id):
        """ Delete subject from db """

        subjects = self.get_all_subjects(author_id=author_id)

        # Search for subject and if exists delete it.
        for subject in subjects:

            if main_subject == subject.subjects_title:
                subject_obj = M.Subjects.query.filter_by(subjects_title=main_subject).first()  # Message to delete

                # Delete
                if subject_obj:
                    delete_subject = self.db.session.get(M.Subjects, subject_obj.id)
                    self.db.session.delete(delete_subject)
                    self.db.session.commit()
                    # If None update
                    return True

    def delete_last_row(self, author_id):
        """ Delete last row from db """

        # Get the last current user message
        last_message_obj = M.Messages.query.filter_by(author_id=author_id). \
            order_by(M.Messages.message_datetime.desc()).first()

        if last_message_obj:
            delete_last_message = self.db.session.get(M.Messages, last_message_obj.message_id)
            self.db.session.delete(delete_last_message)
            self.db.session.commit()

        return last_message_obj

    def add_new_massage(self, data):
        """ Add new message to db """
        Message = M.Messages(message_id=data['message_id'], author_id=data['user_id'], subject=data['subject'],
                             message_datetime=data['message_datetime'], total=data['total'],
                             is_expense=data['is_expense'])

        self.db.session.add(Message)
        self.db.session.commit()
