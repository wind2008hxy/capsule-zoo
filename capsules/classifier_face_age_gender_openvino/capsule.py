from vcap import BaseCapsule, NodeDescription, DeviceMapper
from vcap_utils import BackendRpcProcess

from .backend import Backend
from . import config


class Capsule(BaseCapsule):
    name = "classifier_face_age_gender_openvino"
    description = "OpenVINO face age/gender classifier."
    version = 1
    device_mapper = DeviceMapper.map_to_openvino_devices()
    input_type = NodeDescription(
        size=NodeDescription.Size.SINGLE,
        detections=["face"])
    output_type = NodeDescription(
        size=NodeDescription.Size.SINGLE,
        detections=["face"],
        attributes={"gender": config.genders,
                    "age": list(config.age_bins.values())},
        extra_data=["age", "gender_confidence"]
    )
    backend_loader = lambda capsule_files, device: BackendRpcProcess(
        Backend,
        model_xml=capsule_files[
            "age-gender-recognition-retail-0013.xml"],
        weights_bin=capsule_files[
            "age-gender-recognition-retail-0013.bin"],
        device_name=device
    )
