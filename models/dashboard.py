from datetime import datetime, timezone
from models import db


class Dashboard(db.Model):
    __tablename__ = 'dashboards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, default='')
    icon = db.Column(db.String(10), default='📊')
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    html_content = db.Column(db.Text, default=None)  # Stored in DB for Render compatibility
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    uploaded_at = db.Column(db.DateTime, nullable=True)
    file_size = db.Column(db.Integer, default=0)

    uploader = db.relationship('User', foreign_keys=[uploaded_by])

    @property
    def has_content(self):
        return self.html_content is not None and len(self.html_content) > 0

    @property
    def file_size_display(self):
        if not self.file_size:
            return '-'
        if self.file_size < 1024:
            return f'{self.file_size} B'
        elif self.file_size < 1024 * 1024:
            return f'{self.file_size / 1024:.1f} KB'
        else:
            return f'{self.file_size / (1024 * 1024):.1f} MB'

    @property
    def freshness(self):
        if not self.uploaded_at:
            return 'none'
        now = datetime.now(timezone.utc)
        uploaded = self.uploaded_at.replace(tzinfo=timezone.utc) if self.uploaded_at.tzinfo is None else self.uploaded_at
        diff = (now - uploaded).days
        if diff <= 7:
            return 'fresh'
        elif diff <= 30:
            return 'aging'
        else:
            return 'stale'

    @property
    def updated_display(self):
        if not self.uploaded_at:
            return 'Belum ada data'
        now = datetime.now(timezone.utc)
        diff = now - self.uploaded_at.replace(tzinfo=timezone.utc) if self.uploaded_at.tzinfo is None else now - self.uploaded_at
        if diff.days == 0:
            hours = diff.seconds // 3600
            if hours == 0:
                minutes = diff.seconds // 60
                return f'{minutes} menit lalu' if minutes > 0 else 'Baru saja'
            return f'{hours} jam lalu'
        elif diff.days == 1:
            return 'Kemarin'
        elif diff.days < 7:
            return f'{diff.days} hari lalu'
        else:
            return self.uploaded_at.strftime('%d %b %Y %H:%M')
