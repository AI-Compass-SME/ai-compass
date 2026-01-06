"""empty message

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-01-06 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create company_assessment table
    op.create_table('company_assessment',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_meta', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('questionnaire_id', sa.String(length=100), nullable=False),
        sa.Column('questionnaire_version', sa.String(length=50), nullable=False),
        sa.Column('questionnaire_hash', sa.String(length=64), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_company_assessment_status'), 'company_assessment', ['status'], unique=False)

    # Create questionnaire_response table
    op.create_table('questionnaire_response',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dimension_id', sa.String(length=100), nullable=False),
        sa.Column('question_id', sa.String(length=100), nullable=False),
        sa.Column('answer_type', sa.String(length=50), nullable=False),
        sa.Column('selected_option_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('points_snapshot', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('weight_snapshot', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('answered_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['assessment_id'], ['company_assessment.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questionnaire_response_assessment_id'), 'questionnaire_response', ['assessment_id'], unique=False)
    op.create_index(op.f('ix_questionnaire_response_dimension_id'), 'questionnaire_response', ['dimension_id'], unique=False)
    op.create_index(op.f('ix_questionnaire_response_question_id'), 'questionnaire_response', ['question_id'], unique=False)

    # Create maturity_scores table
    op.create_table('maturity_scores',
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('overall_score', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('overall_level', sa.Integer(), nullable=False),
        sa.Column('dimension_scores', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['assessment_id'], ['company_assessment.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('assessment_id')
    )

    # Create benchmark_cluster_result table
    op.create_table('benchmark_cluster_result',
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('model_version', sa.String(length=50), nullable=False),
        sa.Column('cluster_id', sa.Integer(), nullable=False),
        sa.Column('cluster_label', sa.String(length=100), nullable=False),
        sa.Column('percentile', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('mismatch_flag', sa.Boolean(), nullable=False),
        sa.Column('mismatch_note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['assessment_id'], ['company_assessment.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('assessment_id')
    )

    # Create llm_enrichment_cache table
    op.create_table('llm_enrichment_cache',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('cache_key', sa.String(length=64), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_llm_enrichment_cache_cache_key'), 'llm_enrichment_cache', ['cache_key'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_llm_enrichment_cache_cache_key'), table_name='llm_enrichment_cache')
    op.drop_table('llm_enrichment_cache')
    op.drop_table('benchmark_cluster_result')
    op.drop_table('maturity_scores')
    op.drop_index(op.f('ix_questionnaire_response_question_id'), table_name='questionnaire_response')
    op.drop_index(op.f('ix_questionnaire_response_dimension_id'), table_name='questionnaire_response')
    op.drop_index(op.f('ix_questionnaire_response_assessment_id'), table_name='questionnaire_response')
    op.drop_table('questionnaire_response')
    op.drop_index(op.f('ix_company_assessment_status'), table_name='company_assessment')
    op.drop_table('company_assessment')
