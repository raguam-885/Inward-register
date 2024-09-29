import { Cascader, Select } from "antd";
import React, { useCallback, useEffect, useState } from "react";

const CustomSelect = ({
  id,
  name,
  options,
  value,
  onChange,
  multilevelSelect,
  multipleSelect,
  disabled,
  label,
  isRequired,
}) => {
  const multiSelectOptions = (value, level) => {
    return {
      value: value?.id ? value?.id : value?.name,
      label: value?.name,
      title: value?.name,
      // className: "dropdown-level-" + level,
      children: value?.children?.map((value) =>
        multiSelectOptions(value, level + 1)
      ),
    };
  };

  // Function to transform data to match Cascader options format
  const transformData = (data) => {
    return data.map((item) => ({
      value: item.id,
      label: item.name,
      children: item.children
        ? transformData(
            item.children.map((child) => ({
              value: child.id,  // Set value as the child's id
              label: child.name,
              id: child.id,
              name: child.name,
              children: child.children || [],  // Ensure children is set even if empty
            }))
          )
        : [],
      id: item.name,
      name: item.name,
    }));
  };  

  const [choices, setChoices] = useState([]);
  const [selectedValue, setSelectedValue] = useState("");
console.log("choices are >><<", choices)
  // useEffect(() => {
  //   if (multilevelSelect) {
  //     setChoices(options ? transformData(options) : []);
  //   } else {
  //     const mappedValues = options
  //       ? options.map((each) => ({
  //           value: each?.id ? each?.id : each?.name,
  //           label: each?.name,
  //           title: each?.name,
  //         }))
  //       : [];

  //     setChoices(mappedValues?.length !== 0 ? mappedValues : []);
  //   }
  // }, [id, options, multilevelSelect]);

  useEffect(() => {
    if (multilevelSelect) {
      setChoices(
        options ? transformData(options) : []
      );
      return;
    }

    const mappedValues = options
      ? options?.map((each) => ({
        value: each?.id ? each?.id : each?.name,
        label: each?.name,
        title: each?.name,
      }))
      : [];

    if (mappedValues?.length !== 0) {
      let optionsToBe = isRequired
        ? mappedValues
        : [
          {
            value: "",
            label: `Select`,
          },
          ...mappedValues,
        ]
      setChoices(options ? optionsToBe : []);
    } else {
      setChoices([]);
    }
  }, [id, options, multilevelSelect]);

  const handleChange = useCallback(
    (value, options) => {
      name === "userCreation_department"
        ? onChange({ target: { options, id } })
        : onChange({ target: { id, value } });
      if (multilevelSelect) document.getElementById(id).blur();
    },
    [id, multilevelSelect, name]
  );

  // Recursive function to get all child IDs if a parent node is selected
  const getAllChildIds = (node) => {
    let ids = [];
    if (node.children && node.children.length) {
      node.children.forEach((child) => {
        ids = ids.concat(getAllChildIds(child));
      });
    } else {
      ids.push(node.id);
    }
    return ids;
  };


  const handleMultiLevelSelectChange = (val, selectedOptions = []) => {
    console.log("val on multiLevel Select >><<", val, "selectedOptions >><<", selectedOptions );
    
    let ids = [];

    if (selectedOptions.length > 0) {
      selectedOptions.forEach((option) => {
        if (option.children && option.children.length > 0) {
          ids = ids.concat(getAllChildIds(option));
        } else {
          ids.push(option.value);
        }
      });
    }

    onChange({ target: { id, value: ids } });
  };

  return (
    <React.Fragment>
      {multilevelSelect ? (
        <>
          {label && (
            <label class="form-label">
              {label} {isRequired ? <span className="text-danger">*</span> : ""}
            </label>
          )}
          <Cascader
            id={id}
            name={name}
            options={choices}
            value={value}
            onChange={onChange}
            showSearch={true}
            expandTrigger="hover"
            multiple={multilevelSelect}
            disabled={disabled}
            changeOnSelect={true}
            getPopupContainer={(trigger) => trigger.parentElement}
            fieldNames={{ label: 'name', value: 'id', children: 'children' }} // Added fieldNames prop to correctly map the labels and values
            style={{
              width: "100%",
              height: "50%",
            }}
          />{" "}
        </>
      ) : (
        <>
          {label && (
            <label class="form-label">
              {label} {isRequired ? <span className="text-danger">*</span> : ""}
            </label>
          )}
          <Select
            mode={multipleSelect ? "multiple" : ""}
            // className="form-control"
            id={id}
            showSearch
            optionFilterProp="children"
            onChange={handleChange}
            filterOption={(input, option) =>
              (option?.label ?? "").toLowerCase().includes(input.toLowerCase())
            }
            value={value}
            options={options ? options : ""}
            required={isRequired}
            disabled={disabled}
            getPopupContainer={(trigger) => trigger.parentElement}
            style={{
              width: "100%",
              height: "50%",
            }}
          />
        </>
      )}
    </React.Fragment>
  );
};

export default CustomSelect;
