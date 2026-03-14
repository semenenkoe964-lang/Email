def message_to_dict(message):
    return {
        'id': message.id,
        'sender': message.sender.username,
        'receiver': message.receiver.username,
        'subject': message.subject,
        'body': message.body,
        'folder': message.folder,
        'is_read': message.is_read,
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }