/*jshint esversion: 6 */
export const fieldComponents = [
    {
        type: 'input',
        name: '输入框',
        icon: 'icon-input',
        options: {
            width: '100%',
            defaultValue: '',
            required: false,
            dataType: 'string',
            pattern: '',
            placeholder: '',
            disabled: false,
        }
    },
    {
        type: 'select',
        name: '下拉框',
        icon: 'icon-select',
        options: {
          defaultValue: '',
          multiple: false,
          disabled: false,
          clearable: false,
          placeholder: '',
          required: false,
          showLabel: false,
          width: '',
          options: [
            {
              value: '下拉框1'
            },
            {
              value: '下拉框2'
            },{
              value: '下拉框3'
            }
          ],
          remote: false,
          filterable: false,
          remoteOptions: [],
          props: {
            value: 'value',
            label: 'label'
          },
          remoteFunc: ''
        }
    },
    {
        type: 'radio',
        name: '单选框',
        icon: 'icon-radio-active',
        options: {
          inline: false,
          defaultValue: '',
          showLabel: false,
          options: [
            {
              value: '选项1',
              label: '选项1'
            },
            {
              value: '选项2',
              label: '选项2'
            },
            {
              value: '选项3',
              label: '选项3'
            }
          ],
          required: false,
          width: '',
          remote: false,
          remoteOptions: [],
          props: {
            value: 'value',
            label: 'label'
          },
          remoteFunc: '',
          disabled: false,
        }
      },
]