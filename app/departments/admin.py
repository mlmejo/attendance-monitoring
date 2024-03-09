from flask import Blueprint, flash, redirect, render_template, request

from app.admin.decorators import admin_required
from app.departments.forms import DepartmentForm
from app.models import Department
from app.services import db

admin = Blueprint('departments', __name__)


@admin.route('/departments')
@admin_required
def index():
    departments = Department.query.all()
    return render_template('admin/departments/index.html', departments=departments)


@admin.route('/departments/create', methods=['GET', 'POST'])
@admin_required
def create():
    form = DepartmentForm()

    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        flash('Department created successfully.', 'success')

        return redirect('/admin/departments')

    return render_template('admin/departments/create.html', form=form)


@admin.route('/departments/<int:department_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(department_id):
    department = Department.query.get_or_404(department_id)
    form = DepartmentForm(obj=department)

    if form.validate_on_submit():
        department.name = form.name.data
        db.session.commit()

        flash('Department updated successfully.', 'success')

        return redirect('/admin/departments')

    return render_template('admin/departments/edit.html', department=department, form=form)


@admin.route('/departments/<int:department_id>/delete', methods=['GET', 'POST'])
@admin_required
def destroy(department_id):
    department = Department.query.get_or_404(department_id)

    if request.method == 'POST':
        db.session.delete(department)
        db.session.commit()

        flash('Department deleted successfully.', 'success')

        return redirect('/admin/departments')

    return render_template('admin/departments/delete.html', department=department)
