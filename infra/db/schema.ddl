-- AI-Compass Database Schema
-- PostgreSQL DDL Script
-- Created: 2026-01-09

-- Drop tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS response_items CASCADE;
DROP TABLE IF EXISTS responses CASCADE;
DROP TABLE IF EXISTS answers CASCADE;
DROP TABLE IF EXISTS questionnaire CASCADE;
DROP TABLE IF EXISTS dimensions CASCADE;
DROP TABLE IF EXISTS companies CASCADE;

-- Create dimensions table
CREATE TABLE dimensions (
    dimension_id SERIAL PRIMARY KEY,
    dimension_name VARCHAR(255),
    dimension_weight INTEGER
);

-- Create companies table
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    industry VARCHAR(255),
    website VARCHAR(255),
    number_of_employees VARCHAR(100),
    city VARCHAR(255)
);

-- Create questionnaire table
CREATE TABLE questionnaire (
    question_id SERIAL PRIMARY KEY,
    dimension_id INTEGER,
    header VARCHAR(255),
    question_text VARCHAR(500),
    type VARCHAR(50),
    weight VARCHAR(50),
    optional BOOLEAN,
    CONSTRAINT fk_questionnaire_dimension
        FOREIGN KEY (dimension_id)
        REFERENCES dimensions(dimension_id)
        ON DELETE SET NULL
);

-- Create answers table (predefined answer options)
CREATE TABLE answers (
    answer_id SERIAL PRIMARY KEY,
    question_id INTEGER,
    answer_text VARCHAR(500),
    answer_level INTEGER,
    answer_weight FLOAT,
    CONSTRAINT fk_answers_question
        FOREIGN KEY (question_id)
        REFERENCES questionnaire(question_id)
        ON DELETE CASCADE
);

-- Create responses table (assessment instances)
CREATE TABLE responses (
    response_id SERIAL PRIMARY KEY,
    company_id INTEGER,
    total_score VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_responses_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
        ON DELETE CASCADE
);

-- Create response_items table (actual user answers)
CREATE TABLE response_items (
    item_id SERIAL PRIMARY KEY,
    response_id INTEGER,
    question_id INTEGER,
    answers VARCHAR(500),
    CONSTRAINT fk_response_items_response
        FOREIGN KEY (response_id)
        REFERENCES responses(response_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_response_items_question
        FOREIGN KEY (question_id)
        REFERENCES questionnaire(question_id)
        ON DELETE CASCADE
);

-- Create indexes for performance
CREATE INDEX idx_questionnaire_dimension ON questionnaire(dimension_id);
CREATE INDEX idx_answers_question ON answers(question_id);
CREATE INDEX idx_responses_company ON responses(company_id);
CREATE INDEX idx_response_items_response ON response_items(response_id);
CREATE INDEX idx_response_items_question ON response_items(question_id);

-- Add comments for documentation
COMMENT ON TABLE dimensions IS 'Dimension categories for organizing questions';
COMMENT ON TABLE companies IS 'Company information for assessments';
COMMENT ON TABLE questionnaire IS 'Question definitions with metadata';
COMMENT ON TABLE answers IS 'Predefined answer options for questions';
COMMENT ON TABLE responses IS 'Assessment sessions/responses';
COMMENT ON TABLE response_items IS 'Individual question answers within a response';

COMMENT ON COLUMN questionnaire.type IS 'Question type: single_choice, multiple_choice, slider, boolean, etc.';
COMMENT ON COLUMN questionnaire.optional IS 'Whether the question is optional';
COMMENT ON COLUMN answers.answer_level IS 'Maturity level associated with this answer';
COMMENT ON COLUMN answers.answer_weight IS 'Weight/score for this answer option';
COMMENT ON COLUMN response_items.answers IS 'Selected answer(s) - may be JSON or comma-separated for multiple choice';
