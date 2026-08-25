# Contributing to Student Management System

First off, thank you for considering contributing to the Student Management System! It's people like you that make this project better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to fostering an open and welcoming environment. By participating, you are expected to uphold this standard.

### Our Standards

**Positive behavior includes:**
- Being respectful and inclusive
- Accepting constructive criticism gracefully
- Focusing on what's best for the community
- Showing empathy towards other contributors

**Unacceptable behavior includes:**
- Harassment, discrimination, or inappropriate conduct
- Trolling or insulting comments
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting a bug, include:**
- **Clear title** - Brief description of the issue
- **Steps to reproduce** - Detailed steps to recreate the bug
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Screenshots** - If applicable
- **Environment details** - OS, Python version, Django version
- **Error messages** - Full stack trace if available

**Example:**
```markdown
**Title:** Payment calculation error when student unenrolls from course

**Steps to reproduce:**
1. Create a student and enroll in 2 courses
2. Record a payment
3. Unenroll student from one course
4. Check fee status

**Expected:** Due fee should update automatically
**Actual:** Due fee remains unchanged
**Environment:** Windows 10, Python 3.11, Django 4.2.7
```

### ✨ Suggesting Features

We love feature suggestions! Before suggesting:
- Check if the feature already exists
- Check if it's already been requested
- Consider if it fits the project scope

**Feature request template:**
```markdown
**Feature:** Add email notifications for payment reminders

**Problem it solves:** Students often miss payment deadlines

**Proposed solution:** 
- Send automated email 7 days before due date
- Include payment amount and due date
- Provide payment link

**Alternatives considered:**
- SMS notifications (more expensive)
- In-app notifications only

**Additional context:**
Many educational institutions need this feature
```

### 💻 Contributing Code

We welcome code contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic understanding of Django
- Familiarity with Bootstrap (for UI changes)

### Setting Up Development Environment

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR-USERNAME/student-management-system.git
cd student-management-system

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install development dependencies (optional)
pip install django-debug-toolbar black flake8

# 5. Set up database
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

## Development Workflow

### 1. Create a New Branch

Always create a new branch for your work:

```bash
# For new features
git checkout -b feature/add-email-notifications

# For bug fixes
git checkout -b fix/payment-calculation-error

# For documentation
git checkout -b docs/update-installation-guide
```

### 2. Make Your Changes

- Write clean, readable code
- Follow Django best practices
- Add comments for complex logic
- Update documentation if needed

### 3. Test Your Changes

```bash
# Run the development server
python manage.py runserver

# Test all affected functionality
# - Create test cases if possible
# - Test on different browsers
# - Test responsive design
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "Add email notification feature for payment reminders"
```

### 5. Push to Your Fork

```bash
git push origin feature/add-email-notifications
```

### 6. Create Pull Request

Go to GitHub and create a pull request from your branch.

## Coding Standards

### Python Code Style

We follow **PEP 8** style guide. Key points:

```python
# ✅ Good
def calculate_student_fees(student):
    """Calculate total fees for a student."""
    total = sum(course.fee for course in student.courses.all())
    return total

# ❌ Bad
def calc_fees(s):
    return sum([c.fee for c in s.courses.all()])
```

**Best Practices:**
- Use descriptive variable names
- Keep functions small and focused
- Add docstrings to functions and classes
- Use type hints where appropriate
- Maximum line length: 88 characters (Black formatter)

### Django Conventions

```python
# ✅ Models
class Student(models.Model):
    """Student model with personal and academic information."""
    first_name = models.CharField(max_length=50)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# ✅ Views
@login_required
def student_list(request):
    """Display list of all students."""
    students = Student.objects.select_related('courses').all()
    return render(request, 'student/list.html', {'students': students})
```

### HTML/Template Standards

```django
{# ✅ Good - Semantic HTML, proper indentation #}
<div class="card">
    <div class="card-header">
        <h5 class="mb-0">{{ student.first_name }} {{ student.last_name }}</h5>
    </div>
    <div class="card-body">
        <p>Email: {{ student.email }}</p>
    </div>
</div>

{# ❌ Bad - Poor structure, no indentation #}
<div class="card"><div class="card-header"><h5>{{student.first_name}}</h5></div></div>
```

### JavaScript Standards

```javascript
// ✅ Good - Clear, documented
function updateFeeCalculation() {
    const checkboxes = document.querySelectorAll('input[name="courses"]:checked');
    let totalFee = 0;

    checkboxes.forEach(checkbox => {
        totalFee += parseFloat(checkbox.dataset.fee);
    });

    document.getElementById('totalFee').textContent = `$${totalFee.toFixed(2)}`;
}

// ❌ Bad - Unclear, no documentation
function upd(){var c=document.querySelectorAll('input:checked');var t=0;c.forEach(x=>{t+=parseFloat(x.dataset.fee)});document.getElementById('totalFee').textContent='$'+t.toFixed(2);}
```

## Commit Messages

Write clear, descriptive commit messages following this format:

### Format
```
<type>: <subject>

<body>

<footer>
```

### Types
- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code formatting (no logic change)
- **refactor:** Code restructuring
- **test:** Adding tests
- **chore:** Maintenance tasks

### Examples

```bash
# ✅ Good
feat: Add email notification system for payment reminders

- Implemented automated email sending using Django email backend
- Added email templates for payment reminders
- Created management command to send reminder emails
- Updated settings for email configuration

Closes #45

# ✅ Good
fix: Correct fee calculation when student unenrolls from course

The fee calculation was not updating when a student was removed
from a course. Added signal handler to recalculate fees on
ManyToMany changes.

Fixes #67

# ❌ Bad
update stuff
fixed bug
changes
```

## Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows project style guidelines
- [ ] Comments added for complex code
- [ ] Documentation updated if needed
- [ ] All tests pass
- [ ] No console errors
- [ ] Tested on multiple browsers (if UI changes)
- [ ] Migrations created (if models changed)

### Pull Request Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Related Issue
Closes #XX (if applicable)

## Changes Made
- Change 1
- Change 2
- Change 3

## Screenshots (if applicable)
[Add screenshots here]

## Testing
How to test these changes:
1. Step 1
2. Step 2
3. Expected result

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed my code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Tested thoroughly
```

### Review Process

1. **Automated checks** - Code must pass automated tests
2. **Code review** - Maintainer will review your code
3. **Feedback** - Address any requested changes
4. **Approval** - Once approved, PR will be merged
5. **Merge** - Your contribution becomes part of the project!

## Code Review Guidelines

### For Contributors
- Be open to feedback
- Respond to comments promptly
- Ask questions if unclear
- Be patient during review process

### For Reviewers
- Be constructive and respectful
- Explain reasoning behind suggestions
- Appreciate the contribution
- Focus on the code, not the person

## Areas for Contribution

### High Priority
- [ ] Email notification system
- [ ] PDF report generation
- [ ] Advanced search and filtering
- [ ] Bulk operations (import/export)
- [ ] Multi-language support

### Good First Issues
- [ ] Add validation messages
- [ ] Improve error handling
- [ ] Add more unit tests
- [ ] Update documentation
- [ ] Fix UI inconsistencies

### Future Enhancements
- [ ] Mobile application
- [ ] API development
- [ ] Attendance tracking
- [ ] Grade management
- [ ] Parent portal

## Questions?

If you have questions:
- Check existing documentation
- Search closed issues
- Open a new issue with tag `question`
- Reach out to maintainers

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Credited in project documentation

## Thank You!

Your contributions make this project better. We appreciate your time and effort! 🙏

---

**Happy Contributing!** 🚀

If you need help getting started, feel free to reach out by opening an issue.
