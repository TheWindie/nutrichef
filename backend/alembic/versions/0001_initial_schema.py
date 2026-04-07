"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-08
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('target_kcal', sa.Integer(), nullable=True),
        sa.Column('target_kg', sa.Float(), nullable=True),
        sa.Column('color', sa.String(length=10), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('foods',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_id', sa.String(length=20), nullable=True),
        sa.Column('name_cs', sa.String(length=200), nullable=False),
        sa.Column('name_en', sa.String(length=200), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('energy_kcal', sa.Float(), nullable=False),
        sa.Column('energy_kj', sa.Float(), nullable=True),
        sa.Column('protein_g', sa.Float(), nullable=True),
        sa.Column('carbs_g', sa.Float(), nullable=True),
        sa.Column('fat_g', sa.Float(), nullable=True),
        sa.Column('fiber_g', sa.Float(), nullable=True),
        sa.Column('sugar_g', sa.Float(), nullable=True),
        sa.Column('sat_fat_g', sa.Float(), nullable=True),
        sa.Column('salt_g', sa.Float(), nullable=True),
        sa.Column('water_g', sa.Float(), nullable=True),
        sa.Column('source', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_foods_name_cs', 'foods', ['name_cs'])
    op.create_index('ix_foods_source_id', 'foods', ['source_id'])
    op.create_index('ix_foods_category', 'foods', ['category'])

    op.create_table('meal_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('week_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plan_days',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=True),
        sa.Column('day_of_week', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['plan_id'], ['meal_plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('day_id', sa.Integer(), nullable=True),
        sa.Column('meal_type', sa.Enum('breakfast','lunch','dinner','snack', name='mealtype'), nullable=True),
        sa.Column('name', sa.String(length=300), nullable=False),
        sa.Column('instructions', sa.Text(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['day_id'], ['plan_days.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meal_ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meal_id', sa.Integer(), nullable=True),
        sa.Column('food_id', sa.Integer(), nullable=True),
        sa.Column('amount_radim_g', sa.Float(), nullable=True),
        sa.Column('amount_monika_g', sa.Float(), nullable=True),
        sa.Column('note', sa.String(length=200), nullable=True),
        sa.ForeignKeyConstraint(['food_id'], ['foods.id'], ),
        sa.ForeignKeyConstraint(['meal_id'], ['meals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('meal_ingredients')
    op.drop_table('meals')
    op.drop_table('plan_days')
    op.drop_table('meal_plans')
    op.drop_index('ix_foods_category', table_name='foods')
    op.drop_index('ix_foods_source_id', table_name='foods')
    op.drop_index('ix_foods_name_cs', table_name='foods')
    op.drop_table('foods')
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS mealtype")
