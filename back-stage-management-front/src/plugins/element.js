import Vue from 'vue'
import {Popover,Tree,Option,Select,Switch, Radio, RadioGroup, Drawer, Card,Message,Button, Menu, Submenu, MenuItem, MenuItemGroup, Table, TableColumn, Input, InputNumber, Pagination, Breadcrumb, BreadcrumbItem, Form, FormItem, DatePicker, TimeSelect, TimePicker, Col, Dialog, Dropdown, DropdownMenu, DropdownItem, Tooltip, Container, Header, Aside, Main, Footer, Row, Tag, Checkbox, Link, Divider } from 'element-ui'

Vue.use(Button)
Vue.use(Menu);
Vue.use(Submenu);
Vue.use(MenuItem);
Vue.use(MenuItemGroup);
Vue.use(Table);
Vue.use(TableColumn);
Vue.use(Input);
Vue.use(InputNumber);
Vue.use(Pagination);
Vue.use(Breadcrumb);
Vue.use(BreadcrumbItem);
Vue.use(Form);
Vue.use(FormItem);
Vue.use(DatePicker);
Vue.use(TimeSelect);
Vue.use(TimePicker);
Vue.use(Col);
Vue.use(Dialog);
Vue.use(Dropdown);
Vue.use(DropdownMenu);
Vue.use(DropdownItem);
Vue.use(Tooltip);
Vue.use(Container);
Vue.use(Header);
Vue.use(Aside);
Vue.use(Main);
Vue.use(Footer);
Vue.use(Row);
Vue.use(Tag);
Vue.use(Checkbox);
Vue.use(Link);
Vue.use(Divider);
Vue.use(Card);
Vue.use(Drawer) // ✅ 注册 Drawer 组件
Vue.use(Switch)
Vue.use(Radio)
Vue.use(RadioGroup)
Vue.use(Select)
Vue.use(Option)
Vue.use(Tree)
Vue.use(Popover)

Vue.prototype.$message = Message;