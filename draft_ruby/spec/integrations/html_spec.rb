# frozen_string_literal: true
require 'spec_helper'
require 'draftjs_exporter/html'
require 'draftjs_exporter/entities/link'

RSpec.describe DraftjsExporter::HTML do
  subject(:mapper) do
    described_class.new(
      entity_decorators: {
        'LINK' => DraftjsExporter::Entities::Link.new
      },
      block_map: {
        'header-one' => { element: 'h1' },
        'unordered-list-item' => {
          element: 'li',
          wrapper: ['ul', { className: 'public-DraftStyleDefault-ul' }]
        },
        'unstyled' => { element: 'div' }
      },
      style_map: {
        'ITALIC' => { fontStyle: 'italic' }
      }
    )
  end

  describe '#call' do
    context 'with different blocks' do
      it 'decodes the content_state to html' do
        input = {
          entityMap: {},
          blocks: [
            {
              key: '5s7g9',
              text: 'Header',
              type: 'header-one',
              depth: 0,
              inlineStyleRanges: [],
              entityRanges: []
            },
            {
              key: 'dem5p',
              text: 'some paragraph text',
              type: 'unstyled',
              depth: 0,
              inlineStyleRanges: [],
              entityRanges: []
            }
          ]
        }

        expected_output = <<-OUTPUT.strip
<h1>Header</h1><div>some paragraph text</div>
        OUTPUT

        expect(mapper.call(input)).to eq(expected_output)
      end
    end

    context 'with inline styles' do
      it 'decodes the content_state to html' do
        input = {
          entityMap: {},
          blocks: [
            {
              key: 'dem5p',
              text: 'some paragraph text',
              type: 'unstyled',
              depth: 0,
              inlineStyleRanges: [
                {
                  offset: 0,
                  length: 4,
                  style: 'ITALIC'
                }
              ],
              entityRanges: []
            }
          ]
        }

        expected_output = <<-OUTPUT.strip
<div>
<span style="font-style: italic;">some</span> paragraph text</div>
        OUTPUT

        expect(mapper.call(input)).to eq(expected_output)
      end
    end

    context 'with entities' do
      it 'decodes the content_state to html' do
        input = {
          entityMap: {
            '0' => {
              type: 'LINK',
              mutability: 'MUTABLE',
              data: {
                url: 'http://example.com'
              }
            }
          },
          blocks: [
            {
              key: 'dem5p',
              text: 'some paragraph text',
              type: 'unstyled',
              depth: 0,
              inlineStyleRanges: [],
              entityRanges: [
                {
                  offset: 5,
                  length: 9,
                  key: 0
                }
              ]
            }
          ]
        }

        expected_output = <<-OUTPUT.strip
<div>some <a href="http://example.com">paragraph</a> text</div>
        OUTPUT

        expect(mapper.call(input)).to eq(expected_output)
      end

      it 'throws an error if entities cross over' do
        input = {
          entityMap: {
            '0' => {
              type: 'LINK',
              mutability: 'MUTABLE',
              data: {
                url: 'http://foo.example.com'
              }
            },
            '1' => {
              type: 'LINK',
              mutability: 'MUTABLE',
              data: {
                url: 'http://bar.example.com'
              }
            }
          },
          blocks: [
            {
              key: 'dem5p',
              text: 'some paragraph text',
              type: 'unstyled',
              depth: 0,
              inlineStyleRanges: [],
              entityRanges: [
                {
                  offset: 5,
                  length: 9,
                  key: 0
                },
                {
                  offset: 2,
                  length: 9,
                  key: 1
                }
              ]
            }
          ]
        }

        expect { mapper.call(input) }.to raise_error(DraftjsExporter::InvalidEntity)
      end
    end

    context 'with wrapped blocks' do
      it 'decodes the content_state to html' do
        input = {
          entityMap: {},
          blocks: [
            {
              key: 'dem5p',
              text: 'item1',
              type: 'unordered-list-item',
              depth: 0,
              inlineStyleRanges: [],
              entityRanges: []
            },
            {
              key: 'dem5p',
              text: 'item2',
              type: 'unordered-list-item',
              depth: 0,
              inlineStyleRanges: [],
              entityRanges: []
            }
          ]
        }

        expected_output = <<-EOS.strip
<ul class="public-DraftStyleDefault-ul">\n<li>item1</li>\n<li>item2</li>\n</ul>
EOS

        expect(mapper.call(input)).to eq(expected_output)
      end
    end
  end
end
