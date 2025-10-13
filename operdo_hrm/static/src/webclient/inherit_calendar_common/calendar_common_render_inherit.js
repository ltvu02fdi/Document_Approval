/** @odoo-module **/

import { CalendarCommonRenderer } from "@web/views/calendar/calendar_common/calendar_common_renderer";
import { patch } from "@web/core/utils/patch";
import { renderToString } from "@web/core/utils/render";
import { getColor } from "@web/views/calendar/colors";

const { DateTime } = luxon;

patch(CalendarCommonRenderer.prototype, {
    onEventContent({ event }) {
        const record = this.props.model.records[event.id];
        if (record) {
            // This is needed in order to give the possibility to change the event template.
            const injectedContentStr = renderToString(this.constructor.eventTemplate, {
                ...record,
                startTime: this.getStartTime(record),
                endTime: this.getEndTime(record),
                // Truyền res_model
                res_model: this.props.model.resModel,
            });
            const domParser = new DOMParser();
            const { children } = domParser.parseFromString(injectedContentStr, "text/html").body;
            return { domNodes: children };
        }
        return true;
    },
    eventClassNames({ event }) {
        const classesToAdd = ["o_event"];
        const record = this.props.model.records[event.id];
        const attendance = this.env.searchModel.resModel;
        if (record && attendance !== 'hr.attendance') {
            const color = getColor(record.colorIndex);
            if (typeof color === "number") {
                classesToAdd.push(`o_calendar_color_${color}`);
            } else if (typeof color !== "string") {
                classesToAdd.push("o_calendar_color_0");
            }
            if (record.isHatched) classesToAdd.push("o_event_hatched");
            if (record.isStriked) classesToAdd.push("o_event_striked");
            if (record.duration <= 0.25) classesToAdd.push("o_event_oneliner");
            if (DateTime.now() >= record.end) classesToAdd.push("o_past_event");
            if (!record.isAllDay && !record.isTimeHidden && record.isMonth) {
                classesToAdd.push("o_event_dot");
            } else if (record.isAllDay) {
                classesToAdd.push("o_event_allday");
            }
        }
        else {
            const work_day = record.rawRecord.work_day
            classesToAdd.push(`o_model_attendance`);
            if (work_day === 1) {
                classesToAdd.push(`o_calendar_color_0`);
            } else {
                classesToAdd.push("o_calendar_color_1");
            }
            if (record.isHatched) classesToAdd.push("o_event_hatched");
            if (record.isStriked) classesToAdd.push("o_event_striked");
            if (record.duration <= 0.25) classesToAdd.push("o_event_oneliner");
            if (DateTime.now() >= record.end) classesToAdd.push("o_past_event");
        }
        return classesToAdd;
    },
    onEventMouseEnter(info) {
        const attendance = this.env.searchModel.resModel;
        if(attendance !== 'hr.attendance') {
            this.highlightEvent(info.event, "o_cw_custom_highlight");
        }
    },
    onEventMouseLeave(info) {
        const attendance = this.env.searchModel.resModel;
        if (!info.event.id || attendance ==='hr.attendance') {
            return;
        }
        this.unhighlightEvent(info.event, "o_cw_custom_highlight");
    },
    onClick(info) {
        const attendance = this.env.searchModel.resModel;
        this.openPopover(info.el, this.props.model.records[info.event.id]);
        if(attendance !== 'hr.attendance') {
            this.highlightEvent(info.event, "o_cw_custom_highlight");}
    },
    openPopover(target, record) {
        const attendance = this.env.searchModel.resModel;
        const work_day = record.rawRecord.work_day
        const color = getColor(record.colorIndex);
        if(attendance !== 'hr.attendance') {
            this.popover.open(
                target,
                this.getPopoverProps(record),
                `o_cw_popover card o_calendar_color_${typeof color === "number" ? color : 0}`
            );
        }else{
            this.popover.open(
                target,
                this.getPopoverProps(record),
                `o_cw_popover card o_calendar_color_${work_day === 1 ? 0 : 1}`);
        }
    }

});

